#!/usr/bin/env python3

"""
Given an annotated corpus that we would use as our stacking input and a language
pair (for which we have focus words), figure out which focus words never
actually appear in the stacking-input corpus.
"""

from collections import Counter
import argparse

import annotated_corpus
import list_focus_words
import util

def get_argparser():
    parser = argparse.ArgumentParser(description='stacking_corpus_compare')
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--language_pair', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    util.DPRINT = args.dprint

    top_words = set(list_focus_words.load_top_words(args.language_pair))

    top_words_counts = Counter()
    for sentence in annotated_corpus.generate_sentences(args.annotatedfn):
        for token in sentence:
            if token.lemma in top_words:
                top_words_counts[token.lemma] += 1

    ## TODO: format output sensibly & do reasonable analysis
    # print(top_words_counts)
    print("*" * 80)
    print("focus words that never appear in corpus")
    appearing = set(top_words_counts.keys())
    not_appearing = top_words - appearing
    for word in sorted(not_appearing):
        print(word)

if __name__ == "__main__": main()
