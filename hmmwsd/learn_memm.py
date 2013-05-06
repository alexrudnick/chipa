#!/usr/bin/env python3

import argparse
import random
from collections import defaultdict

import learn
import picklestore

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
    for sent_num in range(10):
        source_sent = []
        target_sent = []
        for i in range(random.randint(5,20)):
            word = random.randint(1, 100)
            source_sent.append("s{0}".format(word)) 
            target_sent.append("t{0}".format(word)) 
        out.append(list(zip(source_sent, target_sent)))
    return out


INSTANCES = defaultdict(list)
def save_instance(instance, word):
    """Store this instance in the training data for this particular word. Later
    we'll replace the defaultdict with a db or something, as needed."""
    INSTANCES[word].append(instance)

def get_instance(tagged_sentence, pos):
    features = {}
    features['pp'] = True

    label = tagged_sentence[pos][1]
    return (features, label)

def extract_instances():
    tagged_sentences = fake_data()

    ## for each sentence...
    for tagged in tagged_sentences:
        ## for each word in that sentence
        for i in range(len(tagged)):
            instance = get_instance(tagged, i)
            save_instance(instance, tagged[i][0])

def main():
    extract_instances()

if __name__ == "__main__": main()
