#!/usr/bin/env python3

"""
Script for generating stats about the most common words in an annotated_corpus.
"""

import argparse
from collections import defaultdict
from collections import Counter

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='mostcommon')
    parser.add_argument('--annotatedfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    surface_count = Counter()
    lemma_count = Counter()
    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    for sentence in source_annotated:
        for token in sentence:
            surface_count[token.surface] += 1
            lemma_count[token.lemma] += 1

    print("%%%% surface")
    for (wordtype, count) in surface_count.most_common(50):
        print("{0} & {1} \\\\".format(wordtype, count))

    print()
    print("%%%% lemmas")
    for (wordtype, count) in lemma_count.most_common(50):
        print("{0} & {1} \\\\".format(wordtype, count))

if __name__ == "__main__": main()
