#!/usr/bin/env python3

import argparse
from operator import itemgetter
import readline


from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import ELEProbDist
from nltk.model import NgramModel

import features
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

def load_bitext():
    """Take in three filenames, return a list of (source,target,alignment)
    lists a list of 3-tuples of lists. Lowercase everything."""
    out_source = []
    out_target = []
    out_align = []

    sourcefn = "/space/output_es_qu/training.es.txt"
    targetfn = "/space/output_es_qu/training.qu.txt"
    alignfn  = "/space/output_es_qu/training.align"

    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align:
        for source, target, alignment in zip(infile_s, infile_t, infile_align):
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
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

def build_instance(tagged_sentence, index):
    feat = features.extract(tagged_sentence, index)
    label = tagged_sentence[index][1]
    return (feat, label)

def repl(sl_sentences, tagged_sentences):
    while True:
        try:
            line = input('> ')
        except: break
        line = line.strip()
        sentences = nltk.sent_tokenize(line)
        s_tokenized = [nltk.word_tokenize(sent) for sent in sentences]
        tokenized = []
        for sent in s_tokenized:
            tokenized.extend(sent)
        print("tokenized:", tokenized)

        answers = []
        ## now for every word in tokenized, we need a classifier.
        classifiers = []
        for word in tokenized:
            ## get all the training data:
            ## need to be doing this from the db rather than linear search
            training = []
            for ss,tagged in zip(sl_sentences, tagged_sentences):
                if word in ss:
                    index = ss.index(word)
                    training.append(build_instance(tagged, index))
            training.append(({'wrong':'wrong'},'wrong'))
            training.append(({'alsowrong':'alsowrong'},'alsowrong'))

            ## XXX: futz with regularization constant here.
            classif = SklearnClassifier(LogisticRegression(C=0.1))
            classif.train(training)
            classifiers.append(classif)

        for i in range(len(tokenized)):
            faketagged = [(w,None) for w in tokenized]
            feat = features.extract(faketagged, i)
            classif = classifiers[i]
            ans = classif.classify(feat)
            answers.append(ans)
        print(list(zip(tokenized, answers)))

def main():
    triple_sentences = load_bitext()
    print("training on {0} sentences.".format(len(triple_sentences)))

    tl_sentences = get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    repl(sl_sentences, tagged_sentences)

if __name__ == "__main__": main()
