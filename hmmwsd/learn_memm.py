#!/usr/bin/env python3

import argparse
import random
import pickle
from collections import defaultdict

import nltk
from nltk.classify.maxent import MaxentClassifier
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import LaplaceProbDist

import learn
import memm_features
import picklestore
import searches
import trainingdb
import util_run_experiment
from constants import CLASSIFIER_THRESHOLD
from constants import EIGHT

def fake_data():
    out = []
    for sent_num in range(1000):
        source_sent = []
        target_sent = []
        for i in range(random.randint(5,20)):
            word = random.randint(1, 10)
            source_sent.append("s{0}".format(word)) 
            target_sent.append("t{0}".format(word)) 
        out.append(list(zip(source_sent, target_sent)))
    return out

INSTANCES = defaultdict(list)
vocabulary = set()
def save_instance(instance, word):
    """Store this instance in the training data for this particular word."""
    trainingdb.save(word, instance)

def build_instance(tagged_sentence, index):
    features = memm_features.extract(tagged_sentence, index)
    label = tagged_sentence[index][1]
    return (features, label)

def extract_instances(tagged_sentences, words_to_include):
    """Get all of the training instances that we're going to need to train the
    classifier, out of the labeled sentences. Store the instances in the
    training db."""
    trainingdb.clear()
    sentnum = 0
    for tagged in tagged_sentences:
        if (sentnum % 10000 ==0):
            print("getting instances from sentence", sentnum)
        savethese = []
        for i in range(len(tagged)):
            word = tagged[i][0]
            if word in words_to_include:
                instance = build_instance(tagged, i)
                savethese.append((word,instance))
        # print("batch saving {0} instances".format(len(savethese)))
        trainingdb.save_many(savethese)
        sentnum += 1

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='hmmwsd')
    parser.add_argument('--sourcetext', type=str, required=True)
    parser.add_argument('--targettext', type=str, required=True)
    parser.add_argument('--targetlang', type=str, required=True)
    parser.add_argument('--alignments', type=str, required=True)
    parser.add_argument('--fast', type=bool, default=False, required=False)
    return parser

def main():
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')
    parser = get_argparser()
    args = parser.parse_args()
    print(args)
    targetlang = args.targetlang
    assert targetlang in util_run_experiment.all_target_languages

    triple_sentences = learn.load_bitext(args)
    print("training on {0} sentences.".format(len(triple_sentences)))
    tl_sentences = learn.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    print("got {0} tagged sentences.".format(len(tagged_sentences)))

    uses = ConditionalFreqDist()
    print("counting uses...")
    for tagged_sent in tagged_sentences:
        for (s,t) in tagged_sent:
            vocabulary.add(s)
            uses[s].inc(t)

    words_to_include = set()
    for word in vocabulary:
        if uses[word].N() > CLASSIFIER_THRESHOLD and uses[word].B() > 1:
            words_to_include.add(word)

    print("words with over", CLASSIFIER_THRESHOLD, "uses:",
          len(words_to_include))

    print("extracting training instances...")
    extract_instances(tagged_sentences, words_to_include)
    
    wordlist_files = []
    for i in range(EIGHT):
        wordlist_files.append(open("WORKLIST/{0}".format(i), "w"))
    for wordnum, sw in enumerate(words_to_include):
        out = wordlist_files[wordnum % EIGHT]
        print(sw, file=out)
    for i in range(EIGHT):
        wordlist_files[i].close()

    ## otherwise: save a big ConditionalProbDist
    uses_cpd = learn.cpd(uses)
    picklefn = "pickles/{0}.uses_cpd.pickle".format(targetlang)
    with open(picklefn, "wb") as outfile:
        pickle.dump(uses_cpd, outfile)
    del uses_cpd

    print("saved everything. done.")

if __name__ == "__main__": main()
