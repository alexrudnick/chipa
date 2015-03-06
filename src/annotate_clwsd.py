#!/usr/bin/env python3

"""
Go over an annotated corpus file and add Brown cluster annotations for the words
in it.
"""

from collections import defaultdict
from operator import itemgetter
import argparse
import os
import sys

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
import nltk

import annotated_corpus
import features
import learn
import trainingdata
import util

def get_argparser():
    parser = argparse.ArgumentParser(description='annotate_clwsd')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    parser.add_argument('--featureprefix', type=str, required=True)
    parser.add_argument('--input', type=str, required=True)
    return parser

## OK, how are we going to do this?
## We need to take a complete Chipa configuration and use this to train
## classifiers on demand. Then we blow through the input annotated corpus and we
## output classifications for that.

def predict_class(sentence, index):
    """Predict a translation for the token at the current index in this
    annotated sentence."""

    ## XXX: see what we've got in learn.py to pull up classifiers on demand.
    ## Maybe it's good, but maybe it needs updates.
    return "foo"

def setup_training_data(args):
    ## XXX: maybe move this to trainingdata.py
    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)

def main():
    parser = get_argparser()
    args = parser.parse_args()
    util.DPRINT = args.dprint

    corpus = annotated_corpus.load_corpus(args.input)
    for sentence in corpus:
        for i, token in enumerate(sentence):
            w = token.lemma
            w = w.lower()
            predicted = predict_class(sentence, i)
            if predicted:
                token.annotations.add(args.featureprefix + "=" + predicted)
            print(token)
        print()

if __name__ == "__main__": main()
