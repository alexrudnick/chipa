#!/usr/bin/env python3

"""
Go over an annotated corpus file and a bunch of CONLL-x formatted parses of
those same sentences and add syntactic features.
"""
import argparse
import copy

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

def find_head_tokens(sentence, parse):
    """For each token in the input sentence, return its syntactic head, if
    any. If its head index is zero, put None in there instead.

    Returns a list of Token objects (or None) of the same length as the input
    sentence.
    """
    out = []
    for token, (headindex, deprel) in zip(sentence, parse):
        if headindex == 0:
            out.append(None)
        else:
            head_token = copy.deepcopy(sentence[headindex - 1])
            out.append(head_token)
    assert(len(out) == len(sentence))
    return out

def find_child_tokens(sentence, parse):
    """For each token in the input sentence, return its syntactic children, if
    any. If it doesn't have any syntactic children, that's fine -- just put an
    empty list in that spot.

    Returns a list of lists of Token objects of the same length as the input
    sentence.
    """
    out = []
    for _ in sentence:
        out.append([])
    for childtoken, (headindex, deprel) in zip(sentence, parse):
        if headindex != 0:
            out[headindex - 1].append(copy.deepcopy(childtoken))
    assert(len(out) == len(sentence))
    return out

def main():
    parser = get_argparser()
    args = parser.parse_args()

    corpus = annotated_corpus.load_corpus(args.annotatedfn)
    parsed_sentences = load_conll(args.conllfn)

    assert len(corpus) == len(parsed_sentences)

    for sentence, parse in zip(corpus, parsed_sentences):
        head_tokens = find_head_tokens(sentence, parse)
        childrens = find_child_tokens(sentence, parse)
        for token,head_token,children in zip(sentence, head_tokens, childrens):
            if head_token:
                head_lemma_annotation = "head_lemma=" + head_token.lemma
                head_surface_annotation = "head_surface=" + head_token.surface
            else:
                head_lemma_annotation = "head_lemma=ROOT"
                head_surface_annotation = "head_surface=ROOT"
            for child_token in children:
                child_lemma_annotation = "child_lemma=" + child_token.lemma
                child_surface_annotation = ("child_surface=" +
                                            child_token.surface)
                token.annotations.add(child_surface_annotation)
                token.annotations.add(child_lemma_annotation)

            token.annotations.add(head_surface_annotation)
            token.annotations.add(head_lemma_annotation)
            print(token)
        print()

if __name__ == "__main__": main()
