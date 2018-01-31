#!/usr/bin/env python3

"""
Go over an annotated corpus file and add CL-WSD predictions for all the tokens
that we can.
"""

from collections import defaultdict
from collections import namedtuple
from operator import itemgetter
import argparse
import os
import sys
import functools

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import nltk

import annotated_corpus
import features
import learn
import list_focus_words
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
    parser.add_argument('--annotated_to_classify', type=str, required=True)
    parser.add_argument('--overwrite', type=bool, default=False, required=True)
    return parser

Filenames = namedtuple("Filenames", ["bitextfn", "alignfn", "annotatedfn"])

## OK, how are we going to do this?
## We need to take a complete Chipa configuration and use this to train
## classifiers on demand. Then we blow through the input annotated corpus and we
## output classifications for that.

#### stuff for loading training data from disk on demand

## XXX: this is copypasta from semeval_experiment.py
def load_training_for_word(word, bitextfn, alignfn, annotatedfn):
    triple_sentences = trainingdata.load_bitext_for_word(word, bitextfn, alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus_for_word(word, annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)
    print("TRAINING DATA LOADED.")

#### end stuff for loading training data from disk on demand

@functools.lru_cache(maxsize=100000)
def classifier_for_lemma(lemma, filenames):
    # XXX: always doing nullable and Random Forest for initial version
    classifier = SklearnClassifier(RandomForestClassifier(), sparse=False)
    print("loading training data for", lemma)
    load_training_for_word(lemma, filenames.bitextfn, filenames.alignfn,
                           filenames.annotatedfn)

    training = trainingdata.trainingdata_for(lemma, nonnull=True)
    print("got {0} instances for {1}".format(len(training), lemma))

    # delete the sentences themselves; we have the instances
    trainingdata.set_examples([], [])
    trainingdata.set_sl_annotated([])

    if len(training) > (60 * 1000):
        print("capping to 60k instances to fit in memory")
        training = training[: 60 * 1000]

    labels = set(label for (feat,label) in training)
    print("loaded training data for", lemma)
    if (not training) or len(labels) < 2:
        return None
    classifier.train(training)
    return classifier

def predict_class(sentence, index, filenames):
    """Predict a translation for the token at the current index in this
    annotated sentence."""

    lemma = sentence[index].lemma
    classifier = classifier_for_lemma(lemma, filenames)
    if not classifier:
        return None

    print("got a classifier for", lemma)

    # tags are just the lemma itself
    tagged_sentence = [(tok.lemma, tok.lemma) for tok in sentence]
    # nltk problem instance

    fs, fakelabel = trainingdata.build_instance(tagged_sentence,
                                                sentence,
                                                index)
    return classifier.classify(fs)

def main():
    parser = get_argparser()
    args = parser.parse_args()
    util.DPRINT = args.dprint

    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)
    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    filenames = Filenames(bitextfn=args.bitextfn,
                          alignfn=args.alignfn,
                          annotatedfn=args.annotatedfn)

    language_pair = args.annotated_to_classify.split(".")[1]
    top_words = set(list_focus_words.load_top_words(language_pair))

    corpus = annotated_corpus.load_corpus(args.annotated_to_classify)
    for sentence in corpus:
        for i, token in enumerate(sentence):
            if token.lemma not in top_words: continue

            predicted = predict_class(sentence, i, filenames)
            if predicted:
                token.annotations.add(args.featureprefix + "=" + predicted)
            if not args.overwrite:
                print(token)
        if not args.overwrite:
            print()

    if args.overwrite:
        with open(args.annotated_to_classify, "w") as outfile:
            for sentence in corpus:
                for i, token in enumerate(sentence):
                    print(token, file=outfile)
                print(file=outfile)


if __name__ == "__main__": main()
