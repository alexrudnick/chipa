#!/usr/bin/env python3

"""
Go over an annotated corpus file and a bunch of CONLL-x formatted parses of
those same sentences and add syntactic features.
"""
import argparse

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='annotate_brown')
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--conllfn', type=str, required=True)
    return parser

def load_conll(conllfn):
    sentences = []
    sentence = []

    with open(conllfn) as infile:
        for line in infile:
            line = line.strip()
            if not line:
                sentences.append(sentence)
                sentence = []
            fields = line.split('\t')
            sentence.append(fields)
            ## TODO: actually parse the fields here
    return sentences

def main():
    parser = get_argparser()
    args = parser.parse_args()

    corpus = annotated_corpus.load_corpus(args.annotatedfn)
    parsed_sentences = load_conll(args.conllfn)

    assert len(corpus) == len(parsed_sentences)

    for sentence in corpus:
        for token in sentence:
            ## TODO: add the features to the token
            print(token)
        print()

if __name__ == "__main__": main()
