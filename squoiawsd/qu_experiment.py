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

import searches
import learn
from preprocess import preprocess

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
            ## hrm, how do we handle alignments in this case?

            #print(line)
            #tagged = searches.maxent_mfs(ss, cfd)
            #print("ORIGINAL:", list(zip(ss,ts)))
            #print("TAGGED:", tagged)
            #predicted = [t for (s,t) in tagged]
            #correct = 0
            #print(list(zip(ts, predicted)))
            #for actual, pred in zip(ts, predicted):
            #    if actual == UNTRANSLATED: continue
            #    totalwords += 1
            #    if actual == pred:
            #        correct += 1
            #        totalcorrect += 1
            #print("sentence accuracy:", correct / len(ss))
            #print("considered words:", len(ss))
    #accuracy = (totalcorrect / totalwords)
    #print("accuracy:", accuracy)
    #print("considered words:", totalwords)

## maybe we want to get the n most common words in the Spanish corpus, and
## cross-validate our classifiers on each of those?

def cross_validate(top_words):
    print("top words:", top_words)
    for w in top_words:
        training = learn.trainingdata_for(w)
        print("*** {0}: {1} instances.".format(w, len(training)))
        if len(training) < 10:
            print("SKIP!")
            continue
        cv = cross_validation.KFold(len(training), n_folds=10, indices=True,
                                    shuffle=False, random_state=None, k=None)
        for traincv, testcv in cv:
            mytraining = training[traincv[0]:traincv[len(traincv)-1]]
            mytesting  = training[testcv[0]:testcv[len(testcv)-1]]

            mfs = learn.MFSClassifier()
            mfs.train(mytraining)
            themfs = mfs.classify({"wrong":"wrong"})
            print("mfs is:", themfs)

            classif = SklearnClassifier(LogisticRegression(C=0.1))
            classif.train(training)
            acc = nltk.classify.util.accuracy(classif, mytesting)
            mfsacc = nltk.classify.util.accuracy(mfs, mytesting)
            print('accuracy:', acc)
            print('mfs accuracy:', mfsacc)

def get_top_words(sl_sentences):
    """Take a list of sentences (each of which is a list of words), return the
    top 100 words."""
    ## TODO: make this just content words. no punctuation, no stopwords
    fd = nltk.probability.FreqDist()
    for sent in sl_sentences:
        for w in sent:
            fd[w] += 1
    mostcommon = fd.most_common(100)
    return [word for (word, count) in mostcommon]

def main():
    parser = learn.get_argparser()

    args = parser.parse_args()
    triple_sentences = learn.load_bitext(args)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    learn.set_examples(sl_sentences,tagged_sentences)

    if args.crossvalidate:
        top_words = get_top_words(sl_sentences)
        cross_validate(top_words)
    else:
        test_on_testset()

if __name__ == "__main__": main()
