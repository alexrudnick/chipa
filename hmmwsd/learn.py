#!/usr/bin/env python3

import argparse
from operator import itemgetter
import pickle
import nltk

import skinnyhmm
import util_run_experiment
import treetagger

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
    tt_home = args.treetaggerhome

    with open(sourcefn) as infile_s, \
         open(targetfn) as infile_t, \
         open(alignfn) as infile_align:
        for source, target, alignment in zip(infile_s, infile_t, infile_align):
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
            count += 1
            if count == (20 * 1000) and fast: break

    out_source = maybe_lemmatize(out_source, "en", tt_home)
    out_target = maybe_lemmatize(out_target, args.targetlang, tt_home)
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
    print("MAYBE LEMMATIZING {0} sentences".format(len(sentences)))
    lemmatizeds = batch_lemmatize_sentences(sentences, language, tt_home)
    out = []
    for (lemmatized, orig) in zip(lemmatizeds, sentences):
        this = []
        for (wl, w) in zip(lemmatized, orig):
            if wl != "<unknown>":
                this.append(wl)
            else:
                this.append(w)
        out.append(this)
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

def get_tagger_and_cfd(args):
    triple_sentences = load_bitext(args)
    print("training on {0} sentences.".format(len(triple_sentences)))
    tagger, cfd = build_tagger_and_cfd(triple_sentences)
    return tagger, cfd

def main():
    parser = get_argparser()
    args = parser.parse_args()
    target = args.targetlang
    assert target in util_run_experiment.all_target_languages
    tagger, cfd = get_tagger_and_cfd(args)
    print(tagger)

    picklefn = "pickles/{0}.tagger.pickle".format(target)
    with open(picklefn, "wb") as outfile:
        pass
        # pickle.dump(tagger, outfile)
    picklefn = "pickles/{0}.cfd.pickle".format(target)
    with open(picklefn, "wb") as outfile:
        pickle.dump(cfd, outfile)

if __name__ == "__main__": main()
