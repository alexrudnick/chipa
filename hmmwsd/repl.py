#!/usr/bin/env python3


import sys
import argparse
import pickle

import nltk

import skinnyhmm
import searches
import learn
import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words
from constants import BEAMWIDTH

def get_argparser():
    parser = argparse.ArgumentParser(description='repl')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.model in ["unigram", "bigram", "trigram"]

    targetlang = args.targetlang
    tt_home = args.treetaggerhome
    model = args.model

    print("Loading models...")
    lm, emissions = None, None

    if model != "unigram":
        picklefn = "pickles/{0}.lm_{1}.pickle".format(targetlang, model)
        with open(picklefn, "rb") as infile:
            lm = pickle.load(infile)

    picklefn = "pickles/{0}.emit.pickle".format(targetlang)
    with open(picklefn, "rb") as infile:
        emissions = pickle.load(infile)
    cfd = learn.reverse_cfd(emissions)
    emissions = learn.cpd(emissions)
    print("OK loaded models.")

    while True:
        try:
            line = input('>')
        except: break
        line = line.strip()
        sentences = nltk.sent_tokenize(line)
        s_tokenized = [nltk.word_tokenize(sent) for sent in sentences]
        tokenized = []
        for sent in s_tokenized: tokenized.extend(sent)
        sss = learn.maybe_lemmatize([tokenized], 'en', tt_home)
        ss = sss[0]
        print(" ".join(ss))
        if model == "unigram":
            tagged = skinnyhmm.mfs(cfd, ss)
        if model == "bigram":
            tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
        elif model == "trigram":
            tagged = searches.beam(lm, emissions, cfd, ss, beamwidth=BEAMWIDTH)
        print(tagged)

if __name__ == "__main__": main()
