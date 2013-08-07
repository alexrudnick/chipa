#!/usr/bin/env python3


import sys
import argparse
from argparse import Namespace
import pickle
import random

import nltk

import guarani
import skinnyhmm
import searches
import learn
import util_run_experiment
from util_run_experiment import output_one_best
from util_run_experiment import output_five_best
from util_run_experiment import all_target_languages
from util_run_experiment import all_words
from util_search import HMMParts
from constants import BEAMWIDTH
from constants import UNTRANSLATED
import stanford

def get_argparser():
    parser = argparse.ArgumentParser(description='repl')
    parser.add_argument('--model', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    parser.add_argument('--randomvalidate', type=bool, required=False,
                        default=True)
    return parser

def repl(model, lm, emissions, cfd):
    while True:
        try:
            line = input('>')
        except: break
        line = line.strip()
        sentences = nltk.sent_tokenize(line)
        s_tokenized = [nltk.word_tokenize(sent) for sent in sentences]
        tokenized = []
        for sent in s_tokenized: tokenized.extend(sent)

        tagger = stanford.get_tagger()
        postags = [t.lower() for (w,t) in tagger.tag(tokenized)]

        sss = learn.maybe_lemmatize([tokenized], 'en', tt_home)
        lemmas = sss[0]
        ss = list(map(nltk.tag.tuple2str, zip(lemmas,postags)))
        print(" ".join(ss))

        if model == "unigram":
            tagged = skinnyhmm.mfs(cfd, ss)
        if model == "bigram":
            tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
        elif model == "trigram":
            tagged = searches.beam(lm, emissions, cfd, ss, beamwidth=BEAMWIDTH)
        print(tagged)

def randomvalidate(model, lm, emissions, cfd):
    args = Namespace()
    args.targetlang="gn"
    args.sourcetext="/space/es_gn_bibles/bible.es.txt" 
    args.targettext="/space/es_gn_bibles/bible.gn.txt"
    args.alignments="/space/output_es_gn/training.align"
    args.fast=False

    triple_sentences = learn.load_bitext(args)
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [source for (source,target,align) in triple_sentences]
    sentence_pairs = list(zip(sl_sentences, tl_sentences))

    hmmparts = HMMParts(lm, emissions, cfd)

    totalcorrect = 0
    totalwords = 0

    for lineid in guarani.testset:
        (ss, ts) = sentence_pairs[lineid]
        print(" ".join(ss))
        if model == "unigram":
            tagged = skinnyhmm.mfs(cfd, ss)
        if model == "bigram":
            tagged = skinnyhmm.viterbi(lm, emissions, cfd, ss)
        elif model == "trigram":
            tagged = searches.beam(lm, emissions, cfd, ss, beamwidth=BEAMWIDTH)
        elif model == "memm":
            tagged = searches.beam_memm(ss, hmmparts, beamwidth=BEAMWIDTH)

        print("ORIGINAL:", list(zip(ss,ts)))
        print("TAGGED:", tagged)

        predicted = [t for (s,t) in tagged]
        correct = 0
        print(list(zip(ts, predicted)))
        for actual, pred in zip(ts, predicted):
            if actual == UNTRANSLATED: continue
            totalwords += 1
            if actual == pred:
                correct += 1
                totalcorrect += 1
        print("sentence accuracy:", correct / len(ss))
        print("considered words:", len(ss))
    accuracy = (totalcorrect / totalwords)
    print("accuracy:", accuracy)
    print("considered words:", totalwords)

def main():
    parser = get_argparser()
    args = parser.parse_args()

    assert args.targetlang in ["es", "gn"]
    assert args.model in ["unigram", "bigram", "trigram", "memm"]

    targetlang = args.targetlang
    tt_home = args.treetaggerhome
    model = args.model
    stanford.taggerhome = "/home/alex/software/stanford-postagger-2012-11-11"

    print("Loading models...")
    lm, emissions = None, None

    if model != "unigram":
        picklefn = "pickles/{0}.lm_{1}.pickle".format(targetlang, "trigram")
        with open(picklefn, "rb") as infile:
            lm = pickle.load(infile)

    picklefn = "pickles/{0}.emit.pickle".format(targetlang)
    with open(picklefn, "rb") as infile:
        emissions = pickle.load(infile)
    cfd = learn.reverse_cfd(emissions)
    emissions = learn.cpd(emissions)
    print("OK loaded models.")

    if not args.randomvalidate:
        repl(model, lm, emissions, cfd)
    else:
        randomvalidate(model, lm, emissions, cfd)

if __name__ == "__main__": main()
