#!/usr/bin/env python3

"""
Script for generating stats about the most common words in a bitext corpus.
"""

import sys
import argparse
from argparse import Namespace
from operator import itemgetter
from collections import defaultdict
from collections import Counter

import nltk

import trainingdata
import clwsd_experiment

def get_argparser():
    parser = argparse.ArgumentParser(description='topwords')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--surfacefn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    clwsd_experiment.STOPWORDS = clwsd_experiment.load_stopwords(args.bitextfn)

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

    top_words = clwsd_experiment.get_top_words(sl_sentences)
    with open("topwords.txt", "w") as topwordsout:
        for (i, (word, count)) in enumerate(top_words):
            print("{0} & {1} & {2} \\\\".format(1+i, word, count),
                  file=topwordsout)

    with open("topwords-translations.txt", "w") as topwordsout:
        for (i, (word, count)) in enumerate(top_words):
            training = trainingdata.trainingdata_for(word, nonnull=False)
            labels = [label for (feat,label) in training]
            counts = Counter(labels)
            translations_l = []
            for label, count in counts.most_common(5):
                translations_l.append("{0} ({1})".format(label, count))
            translations = ", ".join(translations_l)
            print("{0} & {1}".format(word, translations), file=topwordsout)

if __name__ == "__main__": main()
