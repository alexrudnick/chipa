#!/usr/bin/env python3

"""
Go over an annotated corpus file and turn it into CONLL-X format, so we can run
MaltParser over it.
"""
import argparse

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='annotated2connlx')
    parser.add_argument('--annotatedfn', type=str, required=True)
    return parser

def lookup_coarse_tag(tag):
    ## tags are: ADJ ADV INTJ NOUN PROPN VERB
    if tag.startswith("A"):
        return "ADJ"
    if tag.startswith("R"):
        return "ADV"
    if tag.startswith("NC"):
        return "NOUN"
    if tag.startswith("NP"):
        return "PROPN"
    if tag.startswith("VM"):
        return "VERB"
    if tag.startswith("I"):
        return "INTJ"

    ##           ADP AUX CCONJ DET NUM PART PRON SCONJ
    if tag.startswith("VA") or tag.startswith("VS"):
        return "AUX"
    if tag.startswith("S"):
        return "ADP"
    if tag.startswith("P"):
        return "PRON"
    if tag.startswith("CC"):
        return "CCONJ"
    if tag.startswith("CS"):
        return "SCONJ"
    if tag.startswith("D"):
        return "DET"
    if tag.startswith("Z"):
        return "NUM"
    ##           PUNCT SYM X
    if tag.startswith("F"):
        return "PUNCT"
    ## TODO: be able to detect X or SYM?
    return "-"

def main():
    parser = get_argparser()
    args = parser.parse_args()

    corpus = annotated_corpus.load_corpus(args.annotatedfn)

    for sentence in corpus:
        for index, token in enumerate(sentence):
            position = index + 1
            tag = "-"
            for annotation in token.annotations:
                if "=" not in annotation: continue
                k,v = annotation.split("=", maxsplit=1)
                if k == "tag":
                    tag = v

            coarsetag = lookup_coarse_tag(tag)

            # id form lemma cpostag postag feats head deprel phead pdeprel
            print("{0}\t{1}\t{2}\t{3}\t{4}\t-\t-\t-\t-\t-".format(
                position, token.surface, token.lemma, coarsetag, tag))
            ## TODO: use universal pos tags to get coarse tag?
        print()

if __name__ == "__main__": main()
