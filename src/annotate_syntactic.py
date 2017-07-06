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
    """Returns a list of lists, one list per sentence. Each list contains tuples
    of the shape (headindex, deprel). The head indices mark which 1-indexed
    token in this sentence is the current token's head."""
    sentences = []
    sentence = []

    with open(conllfn) as infile:
        for line in infile:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                sentence = []
                continue
            fields = line.split('\t')
            headindex, deprel = fields[6], fields[7]

            # XXX note that these are 1-indexed. 0 indicates having no head or
            # being the ROOT of the sentence.
            headindex = int(headindex)
            sentence.append((headindex, deprel))
    return sentences

def main():
    parser = get_argparser()
    args = parser.parse_args()

    corpus = annotated_corpus.load_corpus(args.annotatedfn)
    parsed_sentences = load_conll(args.conllfn)

    assert len(corpus) == len(parsed_sentences)

    for sentence, parse in zip(corpus, parsed_sentences):
        for token in sentence:
            ## QUICK HACK: clearing out other features for visual clarity
            removethis = None
            for annotation in token.annotations:
                if annotation.startswith("word2vec"):
                    removethis = annotation
            if removethis:
                token.annotations.remove(removethis)
            print(token)
        print()

if __name__ == "__main__": main()
