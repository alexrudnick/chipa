#!/usr/bin/env python3

import sys
import os
from operator import itemgetter 
from collections import defaultdict
from collections import Counter

def langpair(fn):
    name = os.path.basename(fn)
    splitted = name.split("-")
    sl = splitted[5]
    tl = splitted[6]
    return "{0}-{1}".format(sl, tl)

def main():
    show_words = False
    
    # (accuracy, name, word_to_total, word_to_correct)
    file_overviews = []
    for fn in sys.argv[1:]:
        name = os.path.basename(fn)
        lp = langpair(fn)

        word_to_total = Counter()
        word_to_correct = Counter()
        overall_words = 0
        overall_correct = 0

        with open(fn) as infile:
            for line in infile:
                line = line.strip()
                if "\t" not in line: continue
                word, frac, ncorrect, total  = line.split("\t")
                ncorrect = int(ncorrect)
                total = int(total)
                word_to_total[word] += total
                word_to_correct[word] += ncorrect

                overall_correct += ncorrect
                overall_words += total
        overall_accuracy = None
        if overall_words:
            overall_accuracy = overall_correct / overall_words 
            file_overviews.append((overall_accuracy, name,
                                   word_to_correct, word_to_total))

    for (acc, name, w2c, w2t) in sorted(file_overviews, reverse=True):
        print("*" * 80)
        print("{0}\t{1:.3f}".format(name, acc))

        if show_words:
            for word, total in w2t.most_common():
                accuracy = word_to_correct[word] / word_to_total[word]
                print("{0}\t{1}\t{2:.3f}".format(word, total, accuracy))

if __name__ == "__main__": main()