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

import skinnyhmm
import guarani
from skinnyhmm import START
from skinnyhmm import UNTRANSLATED
import util_run_experiment
import treetagger

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

def batch_lemmatize_sentences(sentences, language, tt_home=None):
    """For a list of tokenized sentences in the given language, call TreeTagger
    on them to get a list of lemmas; lowercase them all."""
    codes_to_names = {"en":"english", "de":"german", "it":"italian",
                      "es":"spanish", "fr":"french", "nl":"dutch"}
    tt_lang = codes_to_names[language]
    if tt_lang == 'english':
        tt = treetagger.TreeTagger(tt_home=tt_home,
                                   language=tt_lang,
                                   encoding='latin-1')
    else:
        tt = treetagger.TreeTagger(tt_home=tt_home, language=tt_lang)
    output = tt.batch_tag(sentences)
    return [[lemma.lower() for word,tag,lemma in sent] for sent in output]

def maybe_lemmatize(sentences, language, tt_home=None):
    # print("MAYBE LEMMATIZING {0} sentences".format(len(sentences)))
    lemmatizeds = batch_lemmatize_sentences(sentences, language, tt_home)
    out = []
    for (lemmatized, orig) in zip(lemmatizeds, sentences):
        this = []
        for (wl, w) in zip(lemmatized, orig):
            if wl != "<unknown>":
                this.append(wl.lower())
            else:
                this.append(w.lower())
        out.append(this)
    return out

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

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='hmmwsd')
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--fast', type=bool, default=False, required=False)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    print(args)
    targetlang = args.targetlang
    assert targetlang in ["es", "gn"]

    triple_sentences = load_bitext(args)
    print("training on {0} sentences.".format(len(triple_sentences)))

    ## NB: this is ridiculous, why are we doing this.
    print("source priors")
    source_priors = get_source_priors(triple_sentences)
    picklefn = "pickles/{0}.sourcepriors.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(source_priors, outfile)
    del source_priors

    print("emissions")
    emissions = get_emissions(triple_sentences)
    picklefn = "pickles/{0}.emit.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(emissions, outfile)
    del emissions

    tl_sentences = get_target_language_sentences(triple_sentences)

    print("trigram model")
    lm_trigram = NgramModel(3, tl_sentences, pad_left=True, pad_right=True)
    picklefn = "pickles/{0}.lm_trigram.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(lm_trigram, outfile)
    del lm_trigram

    print("bigram model")
    lm_bigram = NgramModel(2, tl_sentences, pad_left=True, pad_right=True)
    picklefn = "pickles/{0}.lm_bigram.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(lm_bigram, outfile)
    del lm_bigram

    print("done.")

if __name__ == "__main__": main()
