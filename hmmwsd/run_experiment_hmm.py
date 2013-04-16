#!/usr/bin/env python3

import sys
import argparse
import nltk

from learn import get_tagger_and_cfd
import skinnyhmm

import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words

def classify_for_hmm(problem, tagger, cfd):
    """For a given wsd_problem, run the HMM and see what answer we get."""
    print("what's your problem?", problem.tokenized)
    ss = problem.tokenized
    tagged = skinnyhmm.viterbi(tagger, cfd, ss)
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

    ## we'll probably want to move all of this into another file soon (train the
    ## models and pickle them), but for now just leave it here.
    sourcefn = args.sourcetext
    targetfn = args.targettext
    alignmentfn = args.alignments
    fast = args.fast

    tagger,cfd = get_tagger_and_cfd(sourcefn, targetfn, alignmentfn, fast)

    print("Loading test problems...")
    problems = util_run_experiment.get_test_instances(trialdir, sourceword)
    print("OK loaded.")

    ## load or build hmm here or something.

    bestoutfn = "HMMoutput/{0}.{1}.best".format(sourceword, targetlang)
    oofoutfn = "HMMoutput/{0}.{1}.oof".format(sourceword, targetlang)
    with open(bestoutfn, "w") as bestoutfile, \
         open(oofoutfn, "w") as oofoutfile:
        for problem in problems:
            answer = classify_for_hmm(problem, tagger, cfd)
            oof_answers = "uno dos tres quatro cinco".split()
            print(output_one_best(problem, targetlang, answer),
                  file=bestoutfile)
            print(output_five_best(problem, targetlang, oof_answers),
                  file=oofoutfile)

if __name__ == "__main__": main()
