#!/usr/bin/env python3

import sys
import argparse
import nltk

import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words

def main():
    parser = util_run_experiment.get_argparser()
    args = parser.parse_args()
    assert args.targetlang in all_target_languages
    assert args.sourceword in all_words

    targetlang = args.targetlang
    sourceword = args.sourceword
    trialdir = args.trialdir

    print("Loading test problems...")
    problems = util_run_experiment.get_test_instances(trialdir, sourceword)
    print("OK loaded.")

    ## load or build hmm here or something.

    bestoutfn = "HMMoutput/{0}.{1}.best".format(sourceword, targetlang)
    oofoutfn = "HMMoutput/{0}.{1}.oof".format(sourceword, targetlang)
    with open(bestoutfn, "w") as bestoutfile, \
         open(oofoutfn, "w") as oofoutfile:
        for problem in problems:
            # answer = classifier.classify(featureset)
            # dist = classifier.prob_classify(featureset)
            # oof_answers = util_run_experiment.topfive(dist)
            answer = "banco"
            oof_answers = "uno dos tres quatro cinco".split()
            print(output_one_best(problem, targetlang, answer),
                  file=bestoutfile)
            print(output_five_best(problem, targetlang, oof_answers),
                  file=oofoutfile)

if __name__ == "__main__": main()
