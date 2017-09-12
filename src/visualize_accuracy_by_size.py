#!/usr/bin/env python3

import sys
import os
from operator import itemgetter 
from collections import defaultdict
from collections import Counter

import matplotlib.pyplot as plt

def main():
    
    fn = sys.argv[1]
    name = os.path.basename(fn)

    word_to_total = Counter()
    word_to_correct = Counter()

    with open(fn) as infile:
        for line in infile:
            line = line.strip()
            if "\t" not in line: continue
            word, frac, ncorrect, total  = line.split("\t")
            ncorrect = int(ncorrect)
            total = int(total)
            word_to_total[word] += total
            word_to_correct[word] += ncorrect

    totals = []
    accuracies = []
    indices = []

    for index, (word, total) in enumerate(word_to_total.most_common()):
        accuracy = word_to_correct[word] / word_to_total[word]
        print("{0}\t{1}\t{2:.3f}".format(word, total, accuracy))
        indices.append(index)
        totals.append(total)
        accuracies.append(accuracy)

    area = 10
    plt.scatter(indices, accuracies, s=area, alpha=0.5)
    plt.show()

if __name__ == "__main__": main()
