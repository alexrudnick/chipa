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
    return parser

def prettify(elem):
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'unicode')
    ## print(type(rough_string), file=sys.stderr)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_tuples(corpus):
    """Find all the nodes in the tree, return the list of source-language
    tuples."""
    target_nodes = corpus.findall(".//NODE")
    tokens = []
    for node in target_nodes:
        ref = node.attrib['ref']
        try:
            theref = int(ref)
        except:
            util.dprint("REFISNOTINT:", ref)
            theref = int(float(ref))
        sform = node.attrib['sform']
        slem = node.attrib['slem']
        tokens.append((theref, sform, slem))
    tokens.sort()
    return tokens

def make_decision(node, answers):
    """Make a potentially-terrible decision."""
    default = node.attrib['lem']
    option_nodes = [child for child in node if child.tag == 'SYN']
    option_lemmas = ([opt.attrib['lem'] for opt in option_nodes] +
                     [default])

    util.dprint("[DEFAULT]", default)
    util.dprint("[OPTIONS]", " ".join(option_lemmas))

    textref = node.attrib['ref']
    try:
        ref = int(textref)
    except:
        util.dprint("REFISNOTINT:", textref)
        ref = int(float(textref))
        
    chipa_says = answers[ref - 1]
    util.dprint("[CHIPASAYS]", chipa_says)

    ## chipa_says is the list of things in descending order of goodness.
    best = None
    for ans in chipa_says:
        if ans in option_lemmas:
            best = ans
            break

    choice = None
    for child in option_nodes:
        if child.attrib['lem'] == best:
            util.dprint("HOLY COW CLASSIFIER MADE A DECISION")
            choice = child
            break
    if choice is None:
        util.dprint("CLASSIFIER DIDN'T HELP, BAILING")
        return True

    for k,v in choice.attrib.items():
        node.attrib[k] = v
    ## remove the syn nodes.
    for option_node in option_nodes:
        node.remove(option_node)
    return True


@functools.lru_cache(maxsize=100000)
def classifier_for_lemma(lemma):
    # XXX: always doing non-null and Random Forest for initial version
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
        util.dprint("[SURFACE]", " ".join(surface))
        util.dprint("[LEMMAS]", " ".join(lemmas))

        # answers = s.label_sentence(tuples)
        # dprint("[ANSWERS]", answers)
        ## all the NODE elements in the tree that have a SYN underneath
        target_nodes = sentence.findall(".//NODE/SYN/..")
        for node in target_nodes:
            possible_lemmas = set()
            slem = node.attrib["slem"]
            if slem in top_words:
                print("SOURCE LEMMA IN TOP WORDS, GOTTA MAKE A DECISION", slem)
                classifier = classifier_for_lemma(slem)
                if classifier:
                    print("got a classifier!", classifier)

            for syn in node:
                if 'lem' in syn.attrib:
                    possible_lemmas.add(syn.attrib['lem'])
            print(node.attrib["sform"], node.attrib["slem"], possible_lemmas)

        # changed = False
        # for node in target_nodes:
        #     changed_here = make_decision(node, answers)
        #     if changed_here:
        #         changed = True
        # if changed:
        #     dprint("[CLASSIFIERSENTENCE]", sentnum)
    # print(prettify(corpus))

if __name__ == "__main__": main()
