#!/usr/bin/env python3

import argparse
from operator import itemgetter
import nltk

import skinnyhmm

def target_words_for_each_source_word(ss, ts, alignment):
    """Given a list of tokens in source language, a list of tokens in target
    language, and a list of Berkeley-style alignments of the form target-source,
    for each source word, return the list of corresponding target words."""
    alignment = [tuple(map(int, pair.split('-'))) for pair in alignment]
    out = [list() for i in range(len(ss))]
    alignment.sort(key=itemgetter(1))
    for (ti,si) in alignment:
        out[si].append(ts[ti])
    return [" ".join(targetwords) for targetwords in out]

def build_tagger_and_cfd(triple_sentences):
    """Builds the tagger and a conditional freqdist."""

    cfd = nltk.probability.ConditionalFreqDist()
    sentences = []
    for (ss, ts, alignment) in triple_sentences:
        tws = target_words_for_each_source_word(ss, ts, alignment)
        tagged = list(zip(ss, tws))
        ## XXX(alexr): this is sort of ridiculous
        nozeros = [(source, target) for (source,target) in tagged if target]

        for (source, target) in nozeros:
            cfd[source].inc(target)
        # print(nozeros)
        sentences.append(nozeros)

    tagger = nltk.tag.HiddenMarkovModelTagger.train(sentences)
    return tagger, cfd

def load_bitext(sourcefn, targetfn, alignfn, fast=False):
    """Take in three filenames, return a list of (source,target,alignment)
    lists a list of 3-tuples of lists."""
    out_source = []
    out_target = []
    out_align = []
    count = 0
    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align:
        for source, target, alignment in zip(infile_s, infile_t, infile_align):
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
            count += 1
            if count == (20 * 1000) and fast: break
    return list(zip(out_source, out_target, out_align))

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='hmmwsd')
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--fast', type=bool, default=False, required=False)
    return parser

def repl(tagger, cfd):
    while True:
        ss = None
        try:
            ss = input("en> ")
        except:
            pass
        if not ss:
            print()
            return
        ss = ss.lower().split()
        print("source sentence:", ss)
        tagged = skinnyhmm.mfs(tagger, cfd, ss)
        print("mfs:", " ".join([t for (w, t) in tagged]))
        tagged = skinnyhmm.viterbi(tagger, cfd, ss)
        print("viterbi:", " ".join([t for (w, t) in tagged]))

def main():
    parser = get_argparser()
    args = parser.parse_args()

    sourcefn = args.sourcetext
    targetfn = args.targettext
    alignmentfn = args.alignments
    fast = args.fast

    triple_sentences = load_bitext(sourcefn, targetfn, alignmentfn, fast=fast)
    print("training on {0} sentences.".format(len(triple_sentences)))
    tagger, cfd = build_tagger_and_cfd(triple_sentences)

    print(tagger)
    repl(tagger, cfd)

if __name__ == "__main__": main()
