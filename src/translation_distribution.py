#!/usr/bin/env python3

"""
Find script to explore how many times each source word got translated in the
different possible ways.
"""
import argparse

from collections import Counter

import learn
import clwsd_experiment

def get_argparser():
    parser = argparse.ArgumentParser(description='translation_distribution')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    return parser

def possible_translations(w):
    training = learn.trainingdata_for(w, nonnull=False)
    print('word "{0}" has {1} instances'.format(w, len(training)))
    counter = Counter()
    for (feat,label) in training:
        counter[label] += 1
    for (label, count) in counter.most_common():
        print("\t{0}: {1}".format(label, count))

def main():
    parser = get_argparser()
    args = parser.parse_args()

    clwsd_experiment.STOPWORDS = clwsd_experiment.load_stopwords(args.bitextfn)

    triple_sentences = learn.load_bitext_twofiles(args.bitextfn, args.alignfn)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    learn.set_examples(sl_sentences,tagged_sentences)

    top_words = clwsd_experiment.get_top_words(sl_sentences)
    for w in top_words:
        possible_translations(w)

if __name__ == "__main__": main()
