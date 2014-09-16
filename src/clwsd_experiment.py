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
from sklearn.pipeline import Pipeline
from sklearn import cross_validation

import learn
import trainingdata
import brownclusters

def count_correct(classifier, testdata):
    """Given an NLTK-style classifier and some test data, count how many of the
    test instances this classifier gets correct."""
    ## results = classifier.batch_classify([fs for (fs,l) in testdata])
    results = [classifier.classify(fs) for (fs,l) in testdata]
    correct = [l==r for ((fs,l), r) in zip(testdata, results)]
    return correct.count(True)

def cross_validate(top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""

    ## return a map from word to [(accuracy, mfsaccuracy, size)]
    out = defaultdict(list)
    for w in top_words:
        sys.stdout.flush()
        training = trainingdata.trainingdata_for(w, nonnull=nonnull)
        # print('doing word "{0}" with {1} instances'.format(w, len(training)))
        labels = set(label for (feat,label) in training)
        # print("possible labels:", labels)
        if len(labels) < 2:
            print("ONLY ONE SENSE:", w, labels)
            continue
        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=None)
        for traincv, testcv in cv:
            mytraining = training[traincv[0]:traincv[len(traincv)-1]]
            mytesting  = training[testcv[0]:testcv[len(testcv)-1]]

            mfs = learn.MFSClassifier()
            mfs.train(mytraining)

            ## XXX: try l1 regularization and different values of C!
            classif = SklearnClassifier(LogisticRegression(C=1.0, penalty='l2'))
            mytraining = mytraining + [({"absolutelynotafeature":True},
                                        "absolutelynotalabel")]
            classif.train(mytraining)
            ncorrect = count_correct(classif, mytesting)
            ncorrectmfs = count_correct(mfs, mytesting)
            out[w].append((ncorrect,ncorrectmfs,len(mytesting)))
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

def do_a_case(casename, top_words, nonnull):
    print(casename)
    results_table = cross_validate(top_words, nonnull=nonnull)
    print("WEIGHTED ACCURACIES!!")

    ## one entry into these per word
    corrects = []
    mfscorrects = []
    sizes = []
    for w, resultslist in results_table.items():
        for (correct,mfscorrect,size) in resultslist:
            corrects.append(correct)
            mfscorrects.append(mfscorrect)
            sizes.append(size)
    avg = sum(corrects) / sum(sizes)
    mfsavg = sum(mfscorrects) / sum(sizes)
    print("classifiers:", avg)
    print("mfs:", mfsavg)
    # words_with_differences(results_table)

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--surfacefn', type=str, required=True)
    parser.add_argument('--clusterfn', type=str, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    if args.clusterfn:
        brownclusters.set_paths_file(args.clusterfn)

    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    triple_sentences = trainingdata.load_bitext_twofiles(args.bitextfn,
                                                         args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    ## Now we require the surface forms too.
    surface_sentences = trainingdata.load_surface_file(args.surfacefn)
    trainingdata.set_sl_surface_sentences(surface_sentences)

    top_words = trainingdata.get_top_words(sl_sentences)
    top_words = [w for (w,count) in top_words]
    do_a_case("REGULAR", top_words, nonnull=False)
    do_a_case("NONNULL", top_words, nonnull=True)

if __name__ == "__main__": main()
