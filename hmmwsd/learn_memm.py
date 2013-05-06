#!/usr/bin/env python3

import argparse
import random
from collections import defaultdict

import nltk
from nltk.classify.maxent import MaxentClassifier

import learn
import picklestore
import memm_features

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

def fake_data():
    out = []
    for sent_num in range(100):
        source_sent = []
        target_sent = []
        for i in range(random.randint(5,20)):
            word = random.randint(1, 10)
            source_sent.append("s{0}".format(word)) 
            target_sent.append("t{0}".format(word)) 
        out.append(list(zip(source_sent, target_sent)))
    return out


INSTANCES = defaultdict(list)
def save_instance(instance, word):
    """Store this instance in the training data for this particular word. Later
    we'll replace the defaultdict with a db or something, as needed."""
    INSTANCES[word].append(instance)
    print(word, "->", instance)

def get_instances(word):
    return INSTANCES[word]

def build_instance(tagged_sentence, index):
    features = memm_features.extract(tagged_sentence, index)
    label = tagged_sentence[index][1]
    return (features, label)

def extract_instances():
    tagged_sentences = fake_data()

    ## for each sentence...
    for tagged in tagged_sentences:
        ## for each word in that sentence
        for i in range(len(tagged)):
            instance = build_instance(tagged, i)
            save_instance(instance, tagged[i][0])

def main():
    extract_instances()
    vocab = list(INSTANCES.keys())

    for sw in vocab:
        instances = get_instances(sw)
        classifier = MaxentClassifier.train(instances, trace=0)
        picklestore.save(sw, classifier)

    for sw in vocab:
        classifier = picklestore.get(sw)
        print(sw, classifier)

if __name__ == "__main__": main()
