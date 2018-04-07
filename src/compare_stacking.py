#!/usr/bin/env python3

"""
See which features are available on which tokens.
"""

import argparse
import os
import sys

import annotated_corpus
import features
import trainingdata
import util
import list_focus_words

def get_argparser():
    parser = argparse.ArgumentParser(description='compare_stacking')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    util.DPRINT = args.dprint
    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)

    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)

    language_pair = args.bitextfn.split(".")[1]
    top_words = list_focus_words.load_top_words(language_pair)

    print("## GOT THIS MANY TOP WORDS:", len(top_words))
    print("## THEY ARE:", top_words)

    focus_words_with_bible_stacking = set()
    focus_words_with_europarl_stacking = set()

    instances_with_bible_stacking = 0
    instances_with_europarl_stacking = 0
    instances = 0
    for w in top_words:
        training = trainingdata.trainingdata_for(w, nonnull=False)
        labels = set(label for (feat,label) in training)
        if len(labels) < 2:
            continue
        if len(training) < 10:
            print("not enough samples for", w)
            continue

        for (feat_dict, label) in training:
            instances += 1
            has_bible = False
            has_europarl = False
            for k in feat_dict.keys():
                if k.startswith("stacking_"):
                    focus_words_with_europarl_stacking.add(w)
                    has_europarl = True
                elif k.startswith("bible_stacking_"):
                    focus_words_with_bible_stacking.add(w)
                    has_bible = True
            if has_bible:
                instances_with_bible_stacking += 1
            if has_europarl:
                instances_with_europarl_stacking += 1

    print(focus_words_with_bible_stacking)
    print(focus_words_with_europarl_stacking)

    print("this many total instances", instances)
    print("this many with bible", instances_with_bible_stacking)
    print("this many with europarl", instances_with_europarl_stacking)

if __name__ == "__main__": main()
