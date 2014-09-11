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
            print("ONLY ONE SENSE:", w)
            continue
        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=None)
        for traincv, testcv in cv:
            mytraining = training[traincv[0]:traincv[len(traincv)-1]]
            mytesting  = training[testcv[0]:testcv[len(testcv)-1]]

            mfs = learn.MFSClassifier()
            mfs.train(mytraining)

            classif = SklearnClassifier(LogisticRegression(C=0.1))
            mytraining = mytraining + [({"absolutelynotafeature}":True},
                                        "absolutelynotalabel")]
            classif.train(mytraining)
            acc = nltk.classify.util.accuracy(classif, mytesting)
            mfsacc = nltk.classify.util.accuracy(mfs, mytesting)

            out[w].append((acc,mfsacc,len(mytesting)))
    return out

def do_a_case(casename, top_words, nonnull):
    print(casename)
    results_table = cross_validate(top_words, nonnull=nonnull)
    ##save_crossvalidate_results("CROSSVALIDATE-RESULTS-{0}".format(casename),
    ##    results_table)
    print("WEIGHTED ACCURACIES!!")

    ## one entry into these per word
    accuracies = []
    mfsaccuracies = []
    sizes = []
    for w, resultslist in results_table.items():
        totalacc = sum(acc * size for acc,mfsacc,size in resultslist)
        totalmfsacc = sum(mfsacc * size for acc,mfsacc,size in resultslist)
        totalsize = sum(size for acc,mfsacc,size in resultslist)

        ## for this word
        acc = totalacc / totalsize
        mfsacc = totalmfsacc / totalsize
        accuracies.append(acc)
        mfsaccuracies.append(mfsacc)
        sizes.append(totalsize)

    total_acc = sum(accuracies)
    total_mfsacc = sum(mfsaccuracies)
    avg = total_acc / sum(sizes)
    mfsavg = total_mfsacc / sum(sizes)

    print("classifiers:", avg)
    print("mfs:", mfsavg)

    ## get the words with the biggest classifier vs mfs differences
    ## words_with_differences = [(word, acc - mfsacc)
    ##                           for (word, acc, mfsacc)
    ##                           in zip(top_words, accuracies, mfsaccuracies)]
    ## words_with_differences.sort(key=itemgetter(1), reverse=True)
    ## for word, diff in words_with_differences:
    ##     print("{0}\t{1}".format(word,diff))

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
    do_a_case("REGULAR", top_words, nonnull=False)
    do_a_case("NONNULL", top_words, nonnull=True)

if __name__ == "__main__": main()
