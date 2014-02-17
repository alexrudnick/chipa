#!/usr/bin/env python3

import re
import sys

import util

EOS = "#EOS"

from read_morph import get_sentences

def main():
    fn = sys.argv[1]
    sentences = get_sentences(fn)
    util.print_tokenized_sentences(sentences)

if __name__ == "__main__": main()
