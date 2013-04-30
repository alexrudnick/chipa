#!/usr/bin/env python3

import argparse
import nltk
from learn import maybe_lemmatize

def save_lemmas_pretagged(infn, outfn, lang, tt_home):
    sentences_words = []
    sentences_tags = []
    with open(infn) as infile:
        for source in infile:
            tokens = source.strip().lower().split()
            pairs = list(map(nltk.tag.str2tuple, tokens))
            sentences_words.append([w for (w,t) in pairs])
            sentences_tags.append([t for (w,t) in pairs])

    sentences_lemmas = maybe_lemmatize(sentences_words, lang, tt_home)

    with open(outfn, "w") as outfile:
        for sent_lemmas, sent_tags in zip(sentences_lemmas, sentences_tags):
            withtags = list(map(nltk.tag.tuple2str, zip(sent_lemmas,sent_tags)))
            print(" ".join(withtags), file=outfile)

def save_lemmas(infn, outfn, lang, tt_home):
    sentences = []
    with open(infn) as infile:
        for source in infile:
            sentences.append(source.strip().lower().split())
    out = maybe_lemmatize(sentences, lang, tt_home)

    with open(outfn, "w") as outfile:
        for sent in out:
            print(" ".join(sent), file=outfile)

def get_argparser():
    parser = argparse.ArgumentParser(description='preprocess')
    parser.add_argument('--lang', type=str, required=True)
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    parser.add_argument('--pretagged', type=bool, required=True)
    parser.add_argument('--treetaggerhome', type=str, required=False,
                        default="../TreeTagger/cmd")
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    assert args.lang in ["en", "es"] ## , "gn"]

    lang = args.lang
    infn = args.infn
    outfn = args.outfn
    tt_home = args.treetaggerhome
    pretagged = args.treetaggerhome

    ## do it.
    if pretagged:
        save_lemmas_pretagged(infn, outfn, lang, tt_home)
    else:
        save_lemmas(infn, outfn, lang, pretagged, tt_home)

if __name__ == "__main__": main()
