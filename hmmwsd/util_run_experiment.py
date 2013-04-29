#!/usr/bin/env python3

import argparse
import pickle
import os

from parse_test import extract_wsd_problems

all_target_languages = "de es fr it nl".split()
all_words = "bank coach education execution figure job letter match mission mood movement occupation paper passage plant post pot range rest ring scene side soil strain test".split()
final_test_words = "coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test".split()

def output_one_best(problem, target, solution):
    """Return output for a solution for the one-best."""
    return "{0}.{1} {2} :: {3};".format(problem.source_lex,
                                        target,
                                        problem.instance_id,
                                        solution)

def output_five_best(problem, target, solutions):
    """Return output for a solution for the one-best."""
    answerstr = ";".join(solutions)
    return "{0}.{1} {2} ::: {3};".format(problem.source_lex,
                                         target,
                                         problem.instance_id,
                                         answerstr)

def topfive(dist):
    """Given a distribution (the output of running prob_classify), return the
    top five labels in that distribution."""
    probs_and_labels = [(dist.prob(key), key) for key in dist.samples()]
    descending = sorted(probs_and_labels, reverse=True)
    labels = [label for (prob,label) in descending]
    return labels[:5]

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--trialdir', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def get_test_instances(trialdir, sourceword):
    """Given a trialdir and a source word, load up all the problems that we need
    to solve."""
    fn = "{0}/{1}.data".format(trialdir, sourceword)
    return extract_wsd_problems(fn)
