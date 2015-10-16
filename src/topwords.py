#!/usr/bin/env python3

"""
Script for generating stats about the most common words in a bitext corpus.
"""

import sys
import argparse
from collections import defaultdict
from collections import Counter

import nltk

import annotated_corpus
import trainingdata
import clwsd_experiment
import util
from constants import UNTRANSLATED
from entropy import entropy

## sort of a gross hack
import features
features.FEATURES = ["NOFEATURES"]

def get_argparser():
    parser = argparse.ArgumentParser(description='topwords')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    return parser

paperwords = "ser haber decir dios estar hacer tierra ir/ser pueblo pues si así padre señor poner mujer volver poder ir salir judá mismo llevar dicho cielo ojo llegar entrar llamar subir obra hija dejar".split()

def main():
    parser = get_argparser()
    args = parser.parse_args()

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

    with open("topwords.txt", "w") as topwordsout:
        for (i, (word, count)) in enumerate(top_words):
            print("{0} & {1} & {2} \\\\".format(1+i, word, count),
                  file=topwordsout)

    stamp = util.timestamp()
    langs = args.bitextfn.split(".")[1]
    translations_fn = "results/{0}-{1}-translations".format(stamp, langs)
    entropy_fn = "results/{0}-{1}-entropy".format(stamp, langs)

    with open(translations_fn, "w") as topwordsout, \
         open(entropy_fn, "w") as entropyout:
        for (i, (word, count)) in enumerate(top_words):
        ## for (i, word) in enumerate(paperwords):
            training = trainingdata.trainingdata_for(word, nonnull=False)
            labels = [label for (feat,label) in training]
            counts = Counter(labels)
            translations_l = []
            for label, count in counts.most_common(5):
                if label == UNTRANSLATED:
                    label = "NULL"
                translations_l.append("{0}".format(label))
            translations = ", ".join(translations_l)
            print("{0} & {1}".format(word, translations), file=topwordsout)

            bits = entropy(labels)
            if word in paperwords:
                print("%30s%30.2f" % (word, bits), file=entropyout)
            ## print("{0} & {1}".format(word, "%.2f" % bits), 

if __name__ == "__main__": main()
