#!/usr/bin/env python3

"""
Go over an annotated corpus file and add word2vec annotations for the words
in it.
"""
import argparse

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='annotate_brown')
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--embeddingfn', type=str, required=True)
    parser.add_argument('--featureprefix', type=str, required=True)
    return parser

def load_word_to_embeddingstr(embeddingfn):
    out = {}
    with open(embeddingfn) as infile:
        lines = infile.readlines()
    for line in lines[1:]:
        word, embeddingstr = line.strip().split(maxsplit=1)
        out[word] = embeddingstr.replace(" ", "_")
    return out

def main():
    parser = get_argparser()
    args = parser.parse_args()

    word_to_embeddingstr = load_word_to_embeddingstr(args.embeddingfn)
    corpus = annotated_corpus.load_corpus(args.annotatedfn)

    for sentence in corpus:
        for token in sentence:
            w = token.surface
            if w in word_to_embeddingstr:
                embeddingstr = word_to_embeddingstr[w]
                token.annotations.add(args.featureprefix + "=" + embeddingstr)
            print(token)
        print()

if __name__ == "__main__": main()
