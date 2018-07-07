#!/usr/bin/env python3

import argparse
import functools
import os
import sys
import xml.etree.ElementTree as ET

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.ensemble import RandomForestClassifier

import annotated_corpus
import features
import learn
import list_focus_words
import preprocessing
import trainingdata
import util

def get_argparser():
    parser = argparse.ArgumentParser(description='chipa_server')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    parser.add_argument('--outfile', type=str, required=False)
    return parser

def prettify(elem):
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_node_ref(node):
    ref = node.attrib['ref']
    theref = None
    try:
        theref = int(ref)
    except:
        # util.dprint("REFISNOTINT:", ref)
        theref = float(ref)
    return theref

def get_tuples(corpus):
    """Find all the nodes in the tree, return the list of source-language
    tuples."""
    target_nodes = corpus.findall(".//NODE")
    tokens = []
    for node in target_nodes:
        ref = get_node_ref(node)
        sform = node.attrib['sform']
        slem = node.attrib['slem']
        tokens.append((ref, sform, slem))
    tokens.sort()
    return tokens

def remove_mismatch_syns(node, prediction):
    """Remove the syn subnodes that don't match the prediction."""
    syns = [child for child in node if child.tag == 'SYN']
    for syn in syns:
        if syn.attrib['lem'] != prediction:
            node.remove(syn)
            print("WOW ELIMINATED SOME SYNS")

@functools.lru_cache(maxsize=100000)
def classifier_for_lemma(lemma):
    # always doing non-null and Random Forest for initial version
    classifier = SklearnClassifier(RandomForestClassifier(), sparse=False)
    training = trainingdata.trainingdata_for(lemma, nonnull=True)
    print("got {0} instances for {1}".format(len(training), lemma))

    if len(training) > (20 * 1000):
        print("capping to 20k instances to fit in memory")
        training = training[: 20 * 1000]

    labels = set(label for (feat,label) in training)
    print("loaded training data for", lemma)
    if (not training) or len(labels) < 2:
        return None
    classifier.train(training)
    return classifier

def predict_class(classifier, sentence, index):
    """Predict a translation for the token at the current index in this
    annotated sentence."""

    # tags are just the lemma itself
    tagged_sentence = [(tok.lemma, tok.lemma) for tok in sentence]
    # nltk problem instance
    fs, fakelabel = trainingdata.build_instance(tagged_sentence,
                                                sentence,
                                                index)
    return classifier.classify(fs)

def build_sentence(lemmas, surfaces):
    """Return a list of tokens. We should only be given a single sentence at
    once."""
    assert len(lemmas) == len(surfaces)
    sentence = []
    for (lemma, surface) in zip(lemmas, surfaces):
        token = annotated_corpus.Token(lemma, surface)
        sentence.append(token)
    return sentence

def main():
    parser = get_argparser()
    args = parser.parse_args()
    util.DPRINT = args.dprint

    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)
    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    language_pair = args.bitextfn.split(".")[1]
    top_words = set(list_focus_words.load_top_words(language_pair))

    ## Setting up training data...
    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)


    lines = []
    for line in sys.stdin:
        if line.strip():
            lines.append(line.strip())
    corpus = ET.fromstringlist(lines)

    for sentence in corpus:
        sentnum = sentence.attrib['ref']
        tuples = get_tuples(sentence)
        surface = [tup[1] for tup in tuples]
        lemmas = [tup[2] for tup in tuples]
        print("[SURFACE]", " ".join(surface))
        print("[LEMMAS]", " ".join(lemmas))

        ## all the NODE elements in the tree that have a SYN underneath
        target_nodes = sentence.findall(".//NODE/SYN/..")
        for node in target_nodes:
            possible_lemmas = set()
            classifier = None

            slem = node.attrib["slem"]

            if slem in top_words:
                print("SOURCE LEMMA IN TOP WORDS, GOTTA MAKE A DECISION", slem)
                classifier = classifier_for_lemma(slem)
                if classifier:
                    print("got a classifier!", classifier)
            else:
                print("LEMMA NOT IN TOP WORDS, SKIPPING", slem)
                continue

            for syn in node:
                if 'lem' in syn.attrib:
                    possible_lemmas.add(syn.attrib['lem'])

            token_index = None
            for i, tup in enumerate(tuples):
                if tup[0] == get_node_ref(node):
                    token_index = i
            if token_index:
                print("FOUND THE RIGHT NODE", token_index)
            else:
                print("COULD NOT FIND THE RIGHT NODE NO BUENO")

            print("POSSIBILITIES FOR", node.attrib["sform"], node.attrib["slem"], possible_lemmas)
            if classifier and token_index:
                prediction = predict_class(classifier,
                                           build_sentence(lemmas, surface),
                                           token_index)
                print("PREDICTION", prediction)
                if prediction in possible_lemmas:
                    print("HOLY COW PREDICTION IS IN POSSIBLE LEMMAS")

                    remove_mismatch_syns(node, prediction)
                else:
                    print("REGRETTABLE PREDICTION IS NOT IN POSSIBLE LEMMAS")

        # just one sentence for now
        # break
    outfile = sys.stdout
    if args.outfile:
        outfile = open(args.outfile, "w")
    print(prettify(corpus), file=outfile)
    outfile.close()

if __name__ == "__main__": main()
