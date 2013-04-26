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


def classify_for_hmm(problem, lm, emissions, cfd, targetlang, tt_home):
    """For a given wsd_problem, run the HMM and see what answer we get."""
    sss = learn.maybe_lemmatize([problem.tokenized], targetlang, tt_home)
    ss = sss[0]
    ## tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
    tagged = searches.astar(lm, emissions, cfd, ss)
    print(tagged)
    print(tagged[problem.head_indices[0]])
    s,t = tagged[problem.head_indices[0]]
    return t

def main():
    parser = util_run_experiment.get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.sourceword in all_words

    targetlang = args.targetlang
    sourceword = args.sourceword
    trialdir = args.trialdir
    tt_home = args.treetaggerhome

    lm, emissions = None, None
    picklefn = "pickles/{0}.lm.pickle".format(targetlang)
    with open(picklefn, "rb") as infile:
        lm = pickle.load(infile)
    picklefn = "pickles/{0}.emit.pickle".format(targetlang)
    with open(picklefn, "rb") as infile:
        emissions = pickle.load(infile)

    cfd = learn.reverse_cfd(emissions)
    emissions = learn.cpd(emissions)

    print("Loading test problems...")
    problems = util_run_experiment.get_test_instances(trialdir, sourceword)
    print("OK loaded.")

    ## load or build hmm here or something.

    bestoutfn = "HMMoutput/{0}.{1}.best".format(sourceword, targetlang)
    oofoutfn = "HMMoutput/{0}.{1}.oof".format(sourceword, targetlang)
    with open(bestoutfn, "w") as bestoutfile, \
         open(oofoutfn, "w") as oofoutfile:
        for problem in problems:
            answer = classify_for_hmm(problem, lm, emissions, cfd,
                                      targetlang, tt_home)
            oof_answers = "uno dos tres quatro cinco".split()
            print(output_one_best(problem, targetlang, answer),
                  file=bestoutfile)
            print(output_five_best(problem, targetlang, oof_answers),
                  file=oofoutfile)

if __name__ == "__main__": main()
