#!/usr/bin/env python3

import argparse
import random
from collections import defaultdict

import nltk
from nltk.classify.maxent import MaxentClassifier

import learn
import picklestore
import memm_features
import searches
import util_run_experiment

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
def save_instance(instance, word):
    """Store this instance in the training data for this particular word. Later
    we'll replace the defaultdict with a db or something, as needed."""
    INSTANCES[word].append(instance)
    ## print(word, "->", instance)

def get_instances(word):
    return INSTANCES[word]

def build_instance(tagged_sentence, index):
    features = memm_features.extract(tagged_sentence, index)
    label = tagged_sentence[index][1]
    return (features, label)

def extract_instances(tagged_sentences):
    # tagged_sentences = fake_data()
    ## for each sentence...
    for tagged in tagged_sentences:
        ## for each word in that sentence
        for i in range(len(tagged)):
            instance = build_instance(tagged, i)
            save_instance(instance, tagged[i][0])

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

    print("extracting training instances...")
    extract_instances(tagged_sentences)
    vocab = list(INSTANCES.keys())

    for sw in vocab:
        instances = get_instances(sw)
        classifier = MaxentClassifier.train(instances,trace=-1,algorithm='megam')
        picklestore.save(sw, classifier)

    for sw in vocab:
        classifier = picklestore.get(sw)
        print(sw, classifier)

    source_sent = sl_sentences[0]
    tagged = searches.beam_memm(source_sent, 10)
    print("PREDICTED")
    print(tagged)
    print("CORRECT")
    print(tagged_sentences[0])

if __name__ == "__main__": main()
