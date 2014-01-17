#!/usr/bin/env python3

import sys
import util

def get_sentences(fn):
    """Return a list of sentences, where each sentence is a list of tuples.
    This looks like: [ [(token,lemma), (token,lemma)...] ...]"""
    out = []
    with open(fn) as infile:
        sentence = []
        for line in infile:
            lastlineblank = False
            line = line.strip()
            if not line:
                out.append(sentence)
                sentence = []
                continue
                lastlineblank = True
            fields = line.split('\t')
            token, lemma = fields[1], fields[2]
            if lemma in ["[", "]"]: continue
            if lemma.startswith("61,"): continue
            sentence.append((token,lemma))
    if lastlineblank: out.append(sentence)
    return out

def main():
    fn = sys.argv[1]
    sentences = get_sentences(fn)
    util.print_lemmatized_sentences(sentences)

if __name__ == "__main__": main()
