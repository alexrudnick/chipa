#!/usr/bin/env python3

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
import brownclusters
#from preprocess import preprocess

TESTSET="testdata/defensoria1-3_es.txt"

def test_on_testset():
    totalcorrect = 0
    totalwords = 0
    with open(TESTSET) as infile:
        for line in infile:
            ## preprocess that line
            sents = preprocess(line)
            words = []
            if len(sents) > 1:
                print("THIS LINE HAS MULTIPLE SENTENCES.")
            for sent in sents: words.extend(sent.get_words())
            lemmas = [w.get_lemma() for w in words]
            for w,l in zip(words,lemmas):
                print("{0}/{1}".format(w.get_form(),l),end=" ")
            print()

            ## run classifiers over all the lemmas...
            answers = learn.disambiguate_words(lemmas)
            for lemma,t in zip(lemmas,answers):
                print("{0}/{1}".format(lemma,t),end=" ")

def cross_validate(top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""
    accuracies = []
    mfsaccuracies = []
    sizes = []
    for w in top_words:
        sys.stdout.flush()
        training = learn.trainingdata_for(w, nonnull=nonnull)

        if len(training) < 10:
            print("SKIP:", w)
            continue
        labels = set(label for (feat,label) in training)
        if len(labels) < 2:
            print("ONLY ONE SENSE:", w)
            continue

        cv = cross_validation.KFold(len(training), n_folds=10, indices=True,
                                    shuffle=False, random_state=None, k=None)
        for traincv, testcv in cv:
            mytraining = training[traincv[0]:traincv[len(traincv)-1]]
            mytesting  = training[testcv[0]:testcv[len(testcv)-1]]

            mfs = learn.MFSClassifier()
            mfs.train(mytraining)

            classif = SklearnClassifier(LogisticRegression(C=0.1))
            classif.train(mytraining)
            acc = nltk.classify.util.accuracy(classif, mytesting)
            mfsacc = nltk.classify.util.accuracy(mfs, mytesting)

            accuracies.append(acc)
            mfsaccuracies.append(mfsacc)
            sizes.append(len(mytesting))
    return accuracies, mfsaccuracies, sizes

def ispunct(word):
    import string
    punctuations = string.punctuation + "«»¡¿"
    return (word in punctuations or
            all(c in punctuations for c in word))

def get_top_words(sl_sentences):
    """Take a list of sentences (each of which is a list of words), return the
    top 100 words."""
    fd = nltk.probability.FreqDist()
    for sent in sl_sentences:
        for w in sent:
            fd[w] += 1
    mostcommon = fd.most_common(120)
    mostcommon = [word for (word, count) in mostcommon
                  if not ispunct(word)]
    mostcommon = mostcommon[:100]
    return mostcommon

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

def main():
    parser = learn.get_argparser()
    args = parser.parse_args()

    if args.clusterfn:
        brownclusters.set_paths_file(args.clusterfn)

    triple_sentences = learn.load_bitext(args)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    learn.set_examples(sl_sentences,tagged_sentences)

    if not args.crossvalidate:
        test_on_testset()
        return

    top_words = get_top_words(sl_sentences)
    do_a_case("REGULAR", top_words, nonnull=False)
    do_a_case("NONNULL", top_words, nonnull=True)

if __name__ == "__main__": main()
