#!/usr/bin/env python3

"""
Main script for running in-vitro CL-WSD experiments with cross-validation, given
some aligned bitext.
"""

import sys
import argparse
from argparse import Namespace
import pickle
import random

import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import cross_validation

import learn
import trainingdata
import brownclusters

STOPWORDS = None

def cross_validate(top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""
    accuracies = []
    mfsaccuracies = []
    sizes = []
    for w in top_words:
        sys.stdout.flush()
        training = trainingdata.trainingdata_for(w, nonnull=nonnull)

        # print('doing word "{0}" with {1} instances'.format(w, len(training)))

        if len(training) < 10:
            print("SKIP:", w)
            continue
        labels = set(label for (feat,label) in training)
        # print("possible labels:", labels)
        if len(labels) < 2:
            print("ONLY ONE SENSE:", w)
            continue

        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=None)
        for traincv, testcv in cv:
            mytraining = training[traincv[0]:traincv[len(traincv)-1]]
            mytesting  = training[testcv[0]:testcv[len(testcv)-1]]

            mfs = learn.MFSClassifier()
            mfs.train(mytraining)

            classif = SklearnClassifier(LogisticRegression(C=0.1))
            mytraining = mytraining + [({"absolutelynotafeature}":True},
                                        "absolutelynotalabel")]
            classif.train(mytraining)
            acc = nltk.classify.util.accuracy(classif, mytesting)
            mfsacc = nltk.classify.util.accuracy(mfs, mytesting)

            accuracies.append(acc)
            mfsaccuracies.append(mfsacc)
            sizes.append(len(mytesting))
    return accuracies, mfsaccuracies, sizes

def ispunct(word):
    import string
    punctuations = string.punctuation + "«»¡¿—"
    return (word in punctuations or
            all(c in punctuations for c in word))

def get_top_words(sl_sentences):
    """Take a list of sentences (each of which is a list of words), return the
    top 100 words, ignoring punctuation and stopwords."""

    ## What if we just take all the words that occur at least 50 times?
    fd = nltk.probability.FreqDist()
    for sent in sl_sentences:
        for w in sent:
            fd[w] += 1
    mostcommon = fd.most_common()

    out = []
    for (word, count) in mostcommon:
        if word not in STOPWORDS and not ispunct(word):
            if count > 50:
                out.append(word)
            else:
                break
    return out

def save_crossvalidate_results(fn, accuracies, mfsaccuracies, sizes):
    with open(fn, "w") as outfile:
        for a,m,s in zip(accuracies, mfsaccuracies, sizes):
            print("{0}\t{1}\t{2}".format(s,a,m), file=outfile)

def do_a_case(casename, top_words, nonnull):
    print(casename)
    accuracies, mfsaccuracies, sizes = cross_validate(top_words, nonnull=nonnull)
    save_crossvalidate_results("CROSSVALIDATE-RESULTS-{0}".format(casename),
        accuracies, mfsaccuracies, sizes)
    print("WEIGHTED ACCURACIES!!")
    total_acc = sum(a*s for a,s in zip(accuracies, sizes))
    total_mfsacc = sum(m*s for m,s in zip(mfsaccuracies, sizes))
    avg = total_acc / sum(sizes)
    mfsavg = total_mfsacc / sum(sizes)
    print("classifiers:", avg)
    print("mfs:", mfsavg)

def load_stopwords(bitextfn):
    """Determine source language from the input filename."""
    langs = bitextfn.split(".")[1]
    sl = langs.split("-")[0]
    assert sl in ["en", "es"], "wrong sl {0}".format(sl)
    sl = "english" if sl == "en" else "spanish"

    wordtext = nltk.load("corpora/stopwords/{0}".format(sl), format="text")
    wordlist = wordtext.split()
    return set(wordlist)

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--surfacefn', type=str, required=True)
    parser.add_argument('--clusterfn', type=str, required=False)
    return parser

def main():
    global STOPWORDS
    parser = get_argparser()
    args = parser.parse_args()

    if args.clusterfn:
        brownclusters.set_paths_file(args.clusterfn)

    STOPWORDS = load_stopwords(args.bitextfn)

    triple_sentences = trainingdata.load_bitext_twofiles(args.bitextfn,
                                                         args.alignfn)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    ## Now we require the surface forms too.
    surface_sentences = trainingdata.load_surface_file(args.surfacefn)
    trainingdata.set_sl_surface_sentences(surface_sentences)

    top_words = get_top_words(sl_sentences)
    print("TOP WORDS IN SOURCE LANGUAGE", top_words)
    do_a_case("REGULAR", top_words, nonnull=False)
    do_a_case("NONNULL", top_words, nonnull=True)

if __name__ == "__main__": main()
