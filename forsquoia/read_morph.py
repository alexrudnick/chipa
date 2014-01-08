#!/usr/bin/env python3

import sys

import util

EOS = "#EOS"

def get_sentences(fn):
    """Return a list of sentences, where each sentence is a list of tuples.
    This looks like: [ [(token,lemma), (token,lemma)...] ...]"""
    out = []
    with open(fn) as infile:
        sentence = []
        for line in infile:
            line = line.strip()
            if not line: continue
            fields = line.split('\t')
            token, analyzed = fields[0], fields[1]
            lemma = analyzed.split('[')[0]
            if token == EOS:
                out.append(sentence)
                sentence = []
                continue
            sentence.append((token,lemma))
    return out

def main():
    fn = sys.argv[1]
    sentences = get_sentences(fn)
    util.print_lemmatized_sentences(sentences)

if __name__ == "__main__": main()
