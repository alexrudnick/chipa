#!/usr/bin/env python3

"""
Script for running in-vitro CL-WSD experiments with cross-validation, given
some aligned bitext. Here the only feature we use is doc2vec features.

Plan for this is going to look like...

Simple version:
- Train classifiers on the doc2vec vector that we have stored for the sentence.
  That's it.

XXX: This is somewhat messy. We should be making it easier to try adding doc2vec
features in with other features, like in clwsd_experiment.py, or even in the
other embedding experiment file.
"""

from collections import defaultdict
from operator import itemgetter
import argparse
import os
import sys

import numpy as np

from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

import annotated_corpus
import features
import learn
import trainingdata
import util
import list_focus_words

FEATUREPREFIX=None

@util.timeexecution
def cross_validate(classifier, top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""
    ## return a map from word to [(ncorrect,size)]
    out = defaultdict(list)
    util.dprint("cross validating this many words:", len(top_words))

    for w in top_words:
        util.dprint("cross validating:", w)
        doc2vec_labels = trainingdata.doc2vec_labels(w,
                                                     FEATUREPREFIX,
                                                     nonnull=nonnull)
        training = []
        for d2v_string, label in doc2vec_labels:
            sent_vector = np.array([float(x) for x in d2v_string.split("_")])
            training.append((sent_vector, label))

        print("this many instances for {0}: {1}".format(w, len(training)))
        labels = set(label for (feat,label) in training)

        if len(labels) < 2:
            continue
        if len(training) < 10:
            print("not enough samples for", w)
            continue
        ## using constant random_state of 0 for reproducibility
        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=0)
        for traincv, testcv in cv:
            mytraining = [training[i] for i in traincv]
            mytesting = [training[i] for i in testcv]

            mytraining_X = np.array([x for (x, y) in mytraining])
            mytraining_Y = np.array([y for (x, y) in mytraining])

            if len(set(mytraining_Y)) == 1:
                print("only one label, backing off to KNN.")
                classifier = KNeighborsClassifier()

            try:
                classifier.fit(mytraining_X, mytraining_Y) 
            except ValueError as e:
                print("failed out on word:", w)
                print(mytraining_X)
                print(mytraining_Y)
                raise(e)
            print("trained!!", classifier)

            mytesting_X = np.array([x for (x, y) in mytesting])
            mytesting_Y = np.array([y for (x, y) in mytesting])
            predicted = classifier.predict(mytesting_X)
            ncorrect = sum(int(real == pred) for real, pred
                           in zip(mytesting_Y, predicted))
            out[w].append((ncorrect,len(mytesting)))
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
def do_a_case(classifier, top_words, nonnull, casename, stamp):
    print("[[next case]]", casename)
    sys.stdout.flush()
    with open("results/{0}-{1}".format(stamp, casename), "w") as outfile:
        results_table = cross_validate(classifier, top_words, nonnull=nonnull)
        ## one entry into these per word
        corrects = []
        mfscorrects = []
        sizes = []
        for w, resultslist in results_table.items():
            for (correct,size) in resultslist:
                print("{0}\t{1}\t{2}\t{3}".format(
                    w, correct / size, correct, size), file=outfile)
                corrects.append(correct)
                sizes.append(size)
        avg = sum(corrects) / sum(sizes)
        print("accuracy: {0:.4f}".format(avg), file=outfile)

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featureprefix', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def main():
    global FEATUREPREFIX

    parser = get_argparser()
    args = parser.parse_args()

    FEATUREPREFIX = args.featureprefix

    util.DPRINT = args.dprint
    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    print("## RUNNING EXPERIMENT on {0} with features {1}".format(
        os.path.basename(args.bitextfn), "doc2vec"))

    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences, tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)

    language_pair = args.bitextfn.split(".")[1]
    print(language_pair)
    top_words = list_focus_words.load_top_words(language_pair)

    ## default is 1e-4.
    THETOL = 1e-4
    classifier_pairs = []
    classifier = MLPClassifier(solver='lbfgs', alpha=THETOL,
                               hidden_layer_sizes=(20,20))
    classifier_pairs.append(("mlp-20-20", classifier))

    classifier = LogisticRegression(C=1, penalty='l1', tol=THETOL)
    classifier_pairs.append(("maxent-l1-c1", classifier))

    classifier = LogisticRegression(C=1, penalty='l2', tol=THETOL)
    classifier_pairs.append(("maxent-l2-c1", classifier))

    classifier = LinearSVC(C=1, penalty='l2', tol=THETOL)
    classifier_pairs.append(("linearsvc-l2-c1", classifier))

    classifier = RandomForestClassifier()
    classifier_pairs.append(("random-forest-default", classifier))

    classifier = KNeighborsClassifier()
    classifier_pairs.append(("k-neighbors-default", classifier))

    stamp = util.timestamp() + "-" + language_pair
    featureset_name = "doc2vec"

    for (clname, classifier) in classifier_pairs:
        casename = "{0}-{1}-regular".format(clname, featureset_name)
        do_a_case(classifier, top_words, False, casename, stamp)
        casename = "{0}-{1}-nonnull".format(clname, featureset_name)
        do_a_case(classifier, top_words, True, casename, stamp)

if __name__ == "__main__": main()
