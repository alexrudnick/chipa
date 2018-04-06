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

    print("*" * 80)
    print("focus words that never appear in corpus")
    appearing = set(top_words_counts.keys())
    not_appearing = top_words - appearing
    for word in sorted(not_appearing):
        print(word)

    print("*" * 80)
    print("focus words that appear in corpus but <50 times")
    for word, count in top_words_counts.most_common():
        if count in range(1, 50):
            print(word, count)


    atleast50 = set()
    atleast10 = set()
    appearing = set()

    for word in top_words:
        if top_words_counts[word] >= 1:
            appearing.add(word)
        if top_words_counts[word] >= 10:
            atleast10.add(word)
        if top_words_counts[word] >= 50:
            atleast50.add(word)

    ## fraction of words that appear 50 or more times
    print("this many appear >= 50: {} / {} = {:.2}".format(
        len(atleast50), len(top_words), 
        len(atleast50) / len(top_words)))

    ## fraction of words that appear 10 or more times
    print("this many appear >= 10: {} / {} = {:.2}".format(
        len(atleast10), len(top_words), 
        len(atleast10) / len(top_words)))
    
    ## fraction of words that appear 0 times
    never_appear = top_words - appearing
    print("this many never appear: {} / {} = {:.2}".format(
        len(never_appear), len(top_words),
        len(never_appear) / len(top_words)))

if __name__ == "__main__": main()
