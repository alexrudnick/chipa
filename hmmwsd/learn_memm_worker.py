#!/usr/bin/env python3

"""
Train and save classifiers for all the words listed in the input file.
"""

import sys

import nltk
from nltk.classify.maxent import MaxentClassifier
import picklestore
import trainingdb
import random
from constants import MAX_TRAINING_INSTANCES

def get_instances(word):
    return trainingdb.get_all(word)

def main():
    nltk.classify.megam.config_megam(bin='/usr/local/bin/megam')

    with open(sys.argv[1]) as infile:
        lines = infile.readlines()
    words_to_include = [line.strip() for line in lines]

    print("extracting training instances...")
    for wordnum, sw in enumerate(words_to_include):
        instances = get_instances(sw)
        if not instances:
            print("no instances for {0}, skipping".format(sw))
            continue

        if len(instances) > MAX_TRAINING_INSTANCES:
            print("TOO MANY! Sampling {0} down.".format(sw))
            instances = random.sample(instances, MAX_TRAINING_INSTANCES)
            
        print("training", sw, "{0}/{1} with {2} instances".format(
            wordnum, len(words_to_include), len(instances)))
        classifier = MaxentClassifier.train(instances,
                                            trace=0,
                                            max_iter=10,
                                            algorithm='megam')
        picklestore.save(sw, classifier)

if __name__ == "__main__": main()
