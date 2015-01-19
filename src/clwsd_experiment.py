#!/usr/bin/env python3

"""
Main script for running in-vitro CL-WSD experiments with cross-validation, given
some aligned bitext.
"""

import sys
import argparse
from argparse import Namespace
from operator import itemgetter
from collections import defaultdict

import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

import annotated_corpus
import features
import learn
import trainingdata
import util

def count_correct(classifier, testdata):
    """Given an NLTK-style classifier and some test data, count how many of the
    test instances this classifier gets correct."""
    ## results = classifier.batch_classify([fs for (fs,l) in testdata])
    results = [classifier.classify(fs) for (fs,l) in testdata]
    correct = [l==r for ((fs,l), r) in zip(testdata, results)]
    return correct.count(True)

def cross_validate(classifier, top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""
    ## return a map from word to [(ncorrect,size)]
    out = defaultdict(list)
    util.dprint("cross validating this many words:", len(top_words))
    for w in top_words:
        util.dprint("cross validating:", w)
        training = trainingdata.trainingdata_for(w, nonnull=nonnull)
        labels = set(label for (feat,label) in training)
        if len(labels) < 2:
            continue
        if len(training) < 10:
            print("not enough samples for", w)
            continue
        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=None)
        for traincv, testcv in cv:
            mytraining = [training[i] for i in traincv]
            mytesting = [training[i] for i in testcv]
            mytraining = mytraining + [({"absolutelynotafeature":True},
                                        "absolutelynotalabel")]
            classifier.train(mytraining)
            ncorrect = count_correct(classifier, mytesting)
            out[w].append((ncorrect,len(mytesting)))
            ## XXX cut it off after one iteration.
            ## break
    return out

def words_with_differences(results_table):
    """get the words with the biggest classifier vs mfs differences"""
    ## these are going to be the proportion of the cases that classifiers win
    ## over mfs.
    word_diff_pairs = []
    for w, resultslist in results_table.items():
        totalcorrect = sum(correct for (correct,y,z) in resultslist)
        totalmfscorrect = sum(correct for (x,mfscorrect,z) in resultslist)
        totalsize = sum(correct for (x,z,size) in resultslist)
        word_diff_pairs.append((word,
                               (totalcorrect - totalmfscorrect) / totalsize))
    words_with_differences.sort(key=itemgetter(1), reverse=True)
    for word, diff in words_with_differences:
        print("{0}\t{1}".format(word,diff))

## @util.timeexecution
def do_a_case(casename, classifier, top_words, nonnull):
    print("[[next case]]", casename)
    sys.stdout.flush()
    results_table = cross_validate(classifier, top_words, nonnull=nonnull)
    ## one entry into these per word
    corrects = []
    mfscorrects = []
    sizes = []
    for w, resultslist in results_table.items():
        for (correct,size) in resultslist:
            corrects.append(correct)
            sizes.append(size)
    avg = sum(corrects) / sum(sizes)
    print("accuracy: {0:.4f}".format(avg))
    print()
    # words_with_differences(results_table)

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    features.load_featurefile(args.featurefn)

    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)

    top_words = trainingdata.get_top_words(sl_sentences)
    top_words = [w for (w,count) in top_words]

    THETOL = 0.1
    classifier_pairs = []
    classifier_pairs.append(("MFS", learn.MFSClassifier()))

    classifier = SklearnClassifier(LogisticRegression(C=1,
                                   penalty='l2',
                                   tol=THETOL))
    classifier_pairs.append(("maxent-l2-c1", classifier))
    classifier = SklearnClassifier(LinearSVC(C=1, penalty='l2', tol=THETOL))
    classifier_pairs.append(("linearsvc-l2-c1", classifier))
    classifier = SklearnClassifier(RandomForestClassifier(), sparse=False)
    classifier_pairs.append(("random-forest-default", classifier))

    for (name, classifier) in classifier_pairs:
        do_a_case(name + "-regular", classifier, top_words, nonnull=False)

    for (name, classifier) in classifier_pairs:
        do_a_case(name + "-nonnull", classifier, top_words, nonnull=True)

if __name__ == "__main__": main()
