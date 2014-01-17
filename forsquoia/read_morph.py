#!/usr/bin/env python3

import re
import sys

import util

EOS = "#EOS"

pat = re.compile(r"99\d.*\t99\d.*\t[+][?]")
def get_sentences(fn):
    """Return a list of sentences, where each sentence is a list of tuples.
    This looks like: [ [(token,lemma), (token,lemma)...] ...]"""
    out = []
    with open(fn) as infile:
        sentence = []
        for line in infile:
            line = line.strip()

            # skip blank lines
            if not line: continue
            # skip brackets and bible verse numbers.
            if line == "[\t[[$.]": continue
            if line == "]\t][$.]": continue
            if pat.match(line): continue

            fields = line.split('\t')
            try:
                token, analyzed = fields[0], fields[1]
            except:
                print("ERROR!", line, file=sys.stderr)
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
