#!/usr/bin/env python3

"""
Run CL-WSD experiments from semeval2013!
"""

import argparse
import os
import re
from glob import glob

import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

import annotated_corpus
import features
import learn
import trainingdata
import util
import semeval_testset
import preprocessing

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--testset', type=str, required=True)
    parser.add_argument('--outputdir', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def find_head_token_index(annotated, surface, index):
    """Here we are given an annotated sentence, the surface form of the head
    we're looking for, and the index of the particular instance of the thing
    with that surface form that is the head."""

    surface_index = 0
    for i, token in enumerate(annotated):
        if (token.surface == surface or 
            ("_" + surface in token.surface) or
            (surface + "_" in token.surface)):
            if surface_index == index:
                return i
            surface_index += 1
    print(annotated, surface, index)
    assert False, "failed to find head"

def load_training_for_word(word, bitextfn, alignfn, annotatedfn):
    triple_sentences = trainingdata.load_bitext_for_word(word, bitextfn, alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus_for_word(word, annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)
    print("TRAINING DATA LOADED.")


def output_one_best(problem, target, solution):
    """Return output for a solution for the one-best."""
    return "{0}.{1} {2} :: {3};".format(problem[0],
                                        target,
                                        problem[3],
                                        solution)

def output_five_best(problem, target, solutions):
    """Return output for a solution for the one-best."""
    answerstr = ";".join(solutions)
    return "{0}.{1} {2} ::: {3};".format(problem[0],
                                         target,
                                         problem[3],
                                         answerstr)

def topfive(dist):
    """Given a distribution (the output of running prob_classify), return the
    top five labels in that distribution."""
    probs_and_labels = [(dist.prob(key), key) for key in dist.samples()]
    descending = sorted(probs_and_labels, reverse=True)
    labels = [label for (prob,label) in descending]
    return labels[:5]


def main():
    parser = get_argparser()
    args = parser.parse_args()

    util.DPRINT = args.dprint
    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)

    ## default is 1e-4.
    THETOL = 1e-3
    classifier_pairs = []
    classifier_pairs.append(("MFS", learn.MFSClassifier()))

    classifier = SklearnClassifier(LogisticRegression(C=1,
                                   penalty='l2',
                                   tol=THETOL))
    classifier_pairs.append(("maxent-l2-c1", classifier))
    stamp = util.timestamp()

    for fn in glob(args.testset + "/*data"):
        problems = semeval_testset.extract_wsd_problems(fn)

        w = problems[0][0]
        assert w.endswith(".n")
        w = w[:-2]
        load_training_for_word(w, args.bitextfn, args.alignfn, args.annotatedfn)

        bestoutfn = args.outputdir + "/{0}.{1}.best".format(w, "es")
        oofoutfn = args.outputdir + "/{0}.{1}.oof".format(w, "es")
        if os.path.exists(bestoutfn):
            os.remove(bestoutfn)
        if os.path.exists(oofoutfn):
            os.remove(oofoutfn)

        training = None

        for problem in problems:
            w = problem[0]
            assert w.endswith(".n")
            w = w[:-2]
            print(problem)

            if training is None:
                training = trainingdata.trainingdata_for(w, nonnull=True)
                print("got {0} instances for {1}".format(len(training), w))
                labels = set(label for (feat,label) in training)
                if len(training) == 0:
                    print("no samples for", w)
                    break
                if len(labels) < 2:
                    print("there's only one sense for", w, " and it is ",
                          labels)
                    break
                classifier.train(training)

            rawtext = problem[2]
            surface, index = semeval_testset.head_surface_and_index(rawtext)
            replaced = re.sub(r"<head>(.*)</head>", " \\1 ", rawtext)
            annotated = preprocessing.preprocess(replaced, "en")
            sentence = [token.lemma for token in annotated]

            focus_index = find_head_token_index(annotated, surface, index)
            feats = features.extract_untagged(sentence, annotated, focus_index)

            bestoutfn = args.outputdir + "/{0}.{1}.best".format(w, "es")
            oofoutfn = args.outputdir + "/{0}.{1}.oof".format(w, "es")
            with open(bestoutfn, "a") as bestoutfile, \
                 open(oofoutfn, "a") as oofoutfile:

                answer = classifier.classify(feats)
                print(answer)
                dist = classifier.prob_classify(feats)
                oof_answers = topfive(dist)
                print(output_one_best(problem, "es", answer), file=bestoutfile)
                print(output_five_best(problem, "es", oof_answers),
                      file=oofoutfile)

if __name__ == "__main__": main()
