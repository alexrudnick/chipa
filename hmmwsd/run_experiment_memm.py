#!/usr/bin/env python3

import sys
import argparse

import nltk

import searches
import learn
import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words
import util_search
from constants import BEAMWIDTH
from constants import LIKELY_NP

DEBUG=True
def pause():
    if DEBUG: input("ENTER TO CONTINUE")

def classify_for_memm(problem, targetlang, tt_home, model):
    """For a given wsd_problem, run the MEMM and see what answer we get."""
    sss = learn.maybe_lemmatize([problem.tokenized], 'en', tt_home)
    lemmas = sss[0]
    postags = [t for (w,t) in problem.tagged]
    if postags[problem.head_indices[0]] not in LIKELY_NP:
        index = problem.head_indices[0]
        print("FORCING NOUN, was:", problem.tagged[index-2:index+2])
        postags[problem.head_indices[0]] = 'nn'

    ss = list(map(nltk.tag.tuple2str, zip(lemmas,postags)))
    tagged = searches.beam_memm(ss, beamwidth=BEAMWIDTH)
    print(tagged)
    ## if model == "bigram":
    ##     tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
    ## elif model == "trigram":
    ##     tagged = searches.beam(lm, emissions, cfd, ss, beamwidth=BEAMWIDTH)

    # print(tagged[problem.head_indices[0]])
    s,t = tagged[problem.head_indices[0]]
    return t

def main():
    parser = util_run_experiment.get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.model in ["bigram", "trigram"]

    targetlang = args.targetlang
    trialdir = args.trialdir
    tt_home = args.treetaggerhome
    model = args.model

    for sourceword in util_run_experiment.final_test_words:
        print("Loading test problems for {0}".format(sourceword))
        problems = util_run_experiment.get_test_instances(trialdir, sourceword)
        bestoutfn = "MEMMoutput_{0}/{1}.{2}.best".format(
            model, sourceword, targetlang)
        with open(bestoutfn, "w") as bestoutfile:
            for problem in problems:
                answer = classify_for_memm(problem, targetlang, tt_home, model)
                print(output_one_best(problem, targetlang, answer),
                      file=bestoutfile)

if __name__ == "__main__": main()
