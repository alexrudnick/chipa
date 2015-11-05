#!/usr/bin/env python3

"""
Run CL-WSD experiments from semeval2013!
"""

from collections import defaultdict
from operator import itemgetter
import argparse
import os
import sys

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
import semeval_testset

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--testset', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    util.DPRINT = args.dprint
    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)

    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)


    ## default is 1e-4.
    THETOL = 1e-3
    classifier_pairs = []
    classifier_pairs.append(("MFS", learn.MFSClassifier()))

    classifier = SklearnClassifier(LogisticRegression(C=1,
                                   penalty='l1',
                                   tol=THETOL))
    classifier_pairs.append(("maxent-l1-c1", classifier))
    stamp = util.timestamp()

    problems = semeval_testset.extract_wsd_problems(args.testset)
    for problem in problems:
        print(problem)
    # for (clname, classifier) in classifier_pairs:

if __name__ == "__main__": main()
