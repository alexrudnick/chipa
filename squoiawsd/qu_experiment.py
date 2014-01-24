#!/usr/bin/env python3

import sys
import argparse
from argparse import Namespace
import pickle
import random

import nltk

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

def main():
    parser = learn.get_argparser()
    args = parser.parse_args()
    triple_sentences = learn.load_bitext(args)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    learn.set_examples(sl_sentences,tagged_sentences)
    test_on_testset()

if __name__ == "__main__": main()
