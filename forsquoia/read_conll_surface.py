#!/usr/bin/env python3

import sys
import util

from read_conll import get_sentences

def main():
    fn = sys.argv[1]
    sentences = get_sentences(fn)
    util.print_tokenized_sentences(sentences)

if __name__ == "__main__": main()
