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
import util_search
from constants import BEAMWIDTH

def classify_for_hmm(problem, lm, emissions, cfd, targetlang, tt_home, model):
    """For a given wsd_problem, run the HMM and see what answer we get."""
    sss = learn.maybe_lemmatize([problem.tokenized], 'en', tt_home)
    ss = sss[0]
    print(" ".join(problem.tokenized))

    if model == "unigram":
        tagged = skinnyhmm.mfs(cfd, ss)
    if model == "bigram":
        tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
    elif model == "trigram":
        tagged = searches.beam(lm, emissions, cfd, ss, beamwidth=BEAMWIDTH)

    print(tagged[problem.head_indices[0]])
    s,t = tagged[problem.head_indices[0]]
    return t

def main():
    parser = util_run_experiment.get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.model in ["unigram", "bigram", "trigram"]

    targetlang = args.targetlang
    trialdir = args.trialdir
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

    util_search.init_preset_dictionary(targetlang)

    for sourceword in util_run_experiment.final_test_words:
        print("Loading test problems for {0}".format(sourceword))
        problems = util_run_experiment.get_test_instances(trialdir, sourceword)
        bestoutfn = "HMMoutput_{0}/{1}.{2}.best".format(
            model, sourceword, targetlang)
        with open(bestoutfn, "w") as bestoutfile:
            for problem in problems:
                answer = classify_for_hmm(problem, lm, emissions, cfd,
                                          targetlang, tt_home, model)
                print(output_one_best(problem, targetlang, answer),
                      file=bestoutfile)

if __name__ == "__main__": main()
