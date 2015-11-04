#!/usr/bin/env python3

"""
Script for generating stats about the most common words in an annotated_corpus.
"""

import argparse
from collections import defaultdict
from collections import Counter

import annotated_corpus
from trainingdata import ispunct

def get_argparser():
    parser = argparse.ArgumentParser(description='mostcommon')
    parser.add_argument('--annotatedfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    surface_count = Counter()
    lemma_count = Counter()
    total_tokens = 0
    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    for sentence in source_annotated:
        for token in sentence:
            if ispunct(token.surface) or ispunct(token.lemma): continue
            total_tokens += 1
            surface_count[token.surface.lower()] += 1
            lemma_count[token.lemma.lower()] += 1

    print("%%%% surface")
    total_count = 0
    for (wordtype, count) in surface_count.most_common(50):
        total_count += count
        frac = "%0.2f" % (100 * (count / total_tokens))
        cumulative = "%0.2f" % (100 * (total_count / total_tokens))
        print("{0} & {1} & {2} & {3} \\\\".format(wordtype, count, frac,
              cumulative))

    print()
    print("%%%% lemmas")
    total_count = 0
    for (wordtype, count) in lemma_count.most_common(50):
        total_count += count
        frac = "%0.2f" % (100 * (count / total_tokens))
        cumulative = "%0.2f" % (100 * (total_count / total_tokens))
        print("{0} & {1} & {2} & {3} \\\\".format(wordtype, count, frac,
              cumulative))

if __name__ == "__main__": main()
