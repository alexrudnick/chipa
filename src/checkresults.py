#!/usr/bin/env python3

import sys
import os
from operator import itemgetter 
from collections import defaultdict

def getscore(fn):
    """Return score from filename as a float."""
    lines = None
    with open(fn) as infile:
        lines = infile.readlines()
        if len(lines) == 0:
            return 0.0
        assert len(lines) == 1, "wrong number of lines in " + fn
        assert lines[0].startswith("accuracy: ")
    return float(lines[0][len("accuracy: "):])

def langpair(fn):
    name = os.path.basename(fn)
    splitted = name.split("-")
    sl = splitted[5]
    tl = splitted[6]
    return "{0}-{1}".format(sl, tl)

def main():
    ## map from language pair to (regulars, nonnulls)
    ## both of those are lists of pairs of name, score tuples
    allscores = defaultdict(lambda: ([], []))

    for fn in sys.argv[1:]:
        name = os.path.basename(fn)
        lp = langpair(fn)
        if fn.endswith("-regular"):
            allscores[lp][0].append((name, getscore(fn)))
        elif fn.endswith("-nonnull"):
            allscores[lp][1].append((name, getscore(fn)))
        else:
            assert False, "bad filename: " + fn

    for lp in allscores:
        regulars = sorted(allscores[lp][0], key=itemgetter(1), reverse=True)
        nonnulls = sorted(allscores[lp][1], key=itemgetter(1), reverse=True)

        
        print("*** {0} REGULAR ***".format(lp))
        for pair in regulars:
            print("{0}\t{1}".format(*pair))
        print()

        print("*** {0} NONNULL ***".format(lp))
        for pair in nonnulls:
            print("{0}\t{1}".format(*pair))
        print()

if __name__ == "__main__": main()
