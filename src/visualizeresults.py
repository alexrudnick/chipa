#!/usr/bin/env python3

import sys
import os
from operator import itemgetter 
from collections import defaultdict
from collections import Counter

def langpair(fn):
    name = os.path.basename(fn)
    try:
        splitted = name.split("-")
        sl = splitted[5]
        tl = splitted[6]
        return "{0}-{1}".format(sl, tl)
    except:
        print("failed to extract language pair.")
        print("filename:", fn)
        sys.exit(1)

def name_to_setting(name, lp):
    before, after = name.split("-" + lp + "-")
    assert (after.endswith("-regular") or after.endswith("-nonnull"))

    if after.endswith("-regular"):
        return after.split("-regular")[0]
    if after.endswith("-nonnull"):
        return after.split("-nonnull")[0]
    assert False, "this can't happen"


def main():
    # (accuracy, name, word_to_total, word_to_correct)
    file_overviews_regular = []
    file_overviews_nonnull = []

    # Gonna map a classifier setting to a list of 4 numbers.
    # A classifier setting is everything after the language pair in the name but
    # before "-regular" or "-nonnull"
    settings_to_scores = defaultdict(lambda: [0, 0, 0, 0])

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

            setting = name_to_setting(name, lp)

            if lp == "es-gn" and "-regular" in name:
                settings_to_scores[setting][0] = overall_accuracy
            if lp == "es-gn" and "-nonnull" in name:
                settings_to_scores[setting][1] = overall_accuracy
            if lp == "es-qu" and "-regular" in name:
                settings_to_scores[setting][2] = overall_accuracy
            if lp == "es-qu" and "-nonnull" in name:
                settings_to_scores[setting][3] = overall_accuracy

            if "regular" in name:
                file_overviews_regular.append((overall_accuracy, name,
                                               word_to_correct, word_to_total))
            elif "nonnull" in name:
                file_overviews_nonnull.append((overall_accuracy, name,
                                               word_to_correct, word_to_total))

    for setting in sorted(settings_to_scores.keys()):
        scores = settings_to_scores[setting]
        print("{0} & {1:.3f} & {2:.3f} & {3:.3f} & {4:.3f}".format(setting,
              scores[0], scores[1], scores[2], scores[3]))

    print()
    print()
    print("#" * 80)

    for (acc, name, w2c, w2t) in sorted(file_overviews_regular, reverse=True):
        print("{0}\t{1:.3f}".format(name, acc))
        if "MFS" in name:
            print("^^^ MFS baseline ^^^")

    print("*" * 80)
    for (acc, name, w2c, w2t) in sorted(file_overviews_nonnull, reverse=True):
        print("{0}\t{1:.3f}".format(name, acc))
        if "MFS" in name:
            print("^^^ MFS baseline ^^^")

if __name__ == "__main__": main()
