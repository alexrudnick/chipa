#!/usr/bin/env python3

import sys
import argparse
from argparse import Namespace
import pickle
import random

import nltk

import quechua
import skinnyhmm
import searches
import learn
import util_run_experiment
from util_search import HMMParts
from constants import BEAMWIDTH
from constants import UNTRANSLATED

def randomvalidate(model, lm, emissions, cfd):
    totalcorrect = 0
    totalwords = 0
    for lineid in guarani.testset:
        tagged = searches.maxent_mfs(ss, cfd)
        print("ORIGINAL:", list(zip(ss,ts)))
        print("TAGGED:", tagged)
        predicted = [t for (s,t) in tagged]
        correct = 0
        print(list(zip(ts, predicted)))
        for actual, pred in zip(ts, predicted):
            if actual == UNTRANSLATED: continue
            totalwords += 1
            if actual == pred:
                correct += 1
                totalcorrect += 1
        print("sentence accuracy:", correct / len(ss))
        print("considered words:", len(ss))
    accuracy = (totalcorrect / totalwords)
    print("accuracy:", accuracy)
    print("considered words:", totalwords)

def get_argparser():
    parser = argparse.ArgumentParser(description='quechua')
    #parser.add_argument('--model', type=str, required=True)
    #parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    parser.add_argument('--randomvalidate', type=bool, required=False,
                        default=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    assert args.targetlang in ["es", "gn"]
    assert args.model in ["unigram", "bigram", "trigram", "memm", "maxent"]

    targetlang = args.targetlang
    tt_home = args.treetaggerhome
    model = args.model
    stanford.taggerhome = "/home/alex/software/stanford-postagger-2012-11-11"

    randomvalidate(model, lm, emissions, cfd)

if __name__ == "__main__": main()
