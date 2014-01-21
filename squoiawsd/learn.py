#!/usr/bin/env python3

import argparse
from operator import itemgetter
import pickle
import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import ELEProbDist
from nltk.model import NgramModel

from constants import START
from constants import UNTRANSLATED

DEBUG=False
def pause():
    if DEBUG: input("ENTER TO CONTINUE")

import string
punctuations = string.punctuation + "«»¡"
def strip_edge_punctuation(label):
    """Strip out punctuation along the edges. It's pretty bad if this gets into
    the training data."""

    if all((c in string.punctuation) for c in label):
        return label
    ## XXX: this is terrible.
    if label == "@card@":
        return label

    for punc in punctuations:
        if label.startswith(punc):
            ## print("STRIPPED", punc, "FROM", label)
            label = label[1:]
        if label.endswith(punc):
            ## print("STRIPPED", punc, "FROM", label)
            label = label[:1]
    return label

def target_words_for_each_source_word(ss, ts, alignment):
    """Given a list of tokens in source language, a list of tokens in target
    language, and a list of Berkeley-style alignments of the form target-source,
    for each source word, return the list of corresponding target words."""
    alignment = [tuple(map(int, pair.split('-'))) for pair in alignment]
    out = [list() for i in range(len(ss))]
    indices = [list() for i in range(len(ss))]
    alignment.sort(key=itemgetter(0))
    for (ti,si) in alignment:
        ## make sure we're grabbing contiguous phrases
        ## TODO strip punctuation
        if (not indices[si]) or (ti == indices[si][-1] + 1):
            indices[si].append(ti)
            targetword = strip_edge_punctuation(ts[ti])
            out[si].append(targetword)
    return [" ".join(targetwords) for targetwords in out]

def get_emissions(triple_sentences):
    """Return a CFD for the emissions. Note that here we are emitting source
    language words from target language phrases. """
    emissions = ConditionalFreqDist()
    emissions[UNTRANSLATED].inc(UNTRANSLATED)
    for (ss, ts, alignment) in triple_sentences:
        tws = target_words_for_each_source_word(ss, ts, alignment)
        tagged = list(zip(ss, tws))
        if DEBUG:
            print("source sentence:", " ".join(ss))
            print("target sentence:", " ".join(ts))
            print(tagged)
        pause()
        nozeros = [(source, target) for (source,target) in tagged if target]
        for (source, target) in nozeros:
            emissions[target].inc(source)
    return emissions

def get_source_priors(triple_sentences):
    """Return a probability distribution over the individual words in the source
    sentence, which we're going to use later."""

    wordcounts = FreqDist()
    for (ss, ts, alignment) in triple_sentences:
        for sw in ss:
            wordcounts.inc(sw)
    return ELEProbDist(wordcounts)

def get_target_language_sentences(triple_sentences):
    """Return all of the "sentences" over the target language, used for training
    the Source-Order language model."""
    sentences = []
    for (ss, ts, alignment) in triple_sentences:
        tws = target_words_for_each_source_word(ss, ts, alignment)
        sentence = []
        for label in tws:
            if label:
                sentence.append(label)
            else:
                sentence.append(UNTRANSLATED)
        sentences.append(sentence)
    return sentences

def load_bitext(args):
    """Take in three filenames, return a list of (source,target,alignment)
    lists a list of 3-tuples of lists. Lowercase everything."""
    out_source = []
    out_target = []
    out_align = []
    count = 0

    sourcefn = args.sourcetext
    targetfn = args.targettext
    alignfn = args.alignments
    fast = args.fast

    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align:
        for source, target, alignment in zip(infile_s, infile_t, infile_align):
            ## don't skip at test time. FIXME oh geez this is terrible.
            #if count in guarani.testset:
            #    print("SKIP", count)
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
            count += 1
            if count == (1 * 1000) and fast: break

    ## NB: input files should already be lemmatized at this point.
    return list(zip(out_source, out_target, out_align))

def cpd(cfd):
    """Take a ConditionalFreqDist and turn it into a ConditionalProdDist"""
    return ConditionalProbDist(cfd, ELEProbDist)

def reverse_cfd(cfd):
    """Given a ConditionalFreqDist, reverse the conditions and the samples!!"""
    out = ConditionalFreqDist()
    for condition in cfd.conditions():
        for sample in cfd[condition].samples():
            out[sample].inc(condition, cfd[condition][sample])
    return out

def main():
    print("emissions")
    emissions = get_emissions(triple_sentences)
    picklefn = "pickles/{0}.emit.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(emissions, outfile)
    del emissions

    tl_sentences = get_target_language_sentences(triple_sentences)

    print("done.")

if __name__ == "__main__": main()
