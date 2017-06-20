#!/usr/bin/env python3

"""
Extract the list of words for which we want to build classifiers, so we don't
have to do this over and over again in other scripts.
"""

import argparse

import trainingdata

def load_top_words(langpair):
    out = []
    with open("focus_words/" + langpair) as infile:
        for line in infile:
            out.append(line.strip())
    return out

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)
    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]

    top_words = trainingdata.get_top_words(sl_sentences)
    top_words = [w for (w,count) in top_words]

    for tw in top_words:
        print(tw)

if __name__ == "__main__": main()
