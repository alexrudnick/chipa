#!/usr/bin/env python3

import argparse
from operator import itemgetter
import pickle

import nltk
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import ELEProbDist
from nltk.model import NgramModel

import learn
import skinnyhmm
from skinnyhmm import START
from skinnyhmm import UNTRANSLATED
import util_run_experiment

DEBUG=False
def pause():
    if DEBUG: input("ENTER TO CONTINUE")

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='memmwsd')
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--fast', type=bool, default=False, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    triple_sentences = learn.load_bitext(args)
    print("loaded bitext!")
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    print("built target-language sentences!")
    sl_sentences = [source for (source,target,align) in triple_sentences]

    with open("europarl.seq", "w") as outfile:
        for (ss,ts) in zip(sl_sentences, tl_sentences):
            for sw,label in zip(ss,ts):
                label = label.replace(' ', '~')
                print("{0}\t{1}".format(sw, label), file=outfile)
            print(file=outfile)

if __name__ == "__main__": main()
