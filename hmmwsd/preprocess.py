#!/usr/bin/env python3

import argparse
from learn import maybe_lemmatize


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

    ## do it.
    save_lemmas(infn, outfn, lang, tt_home)

if __name__ == "__main__": main()
