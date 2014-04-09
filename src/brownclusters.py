#!/usr/bin/env python3

from collections import defaultdict
from constants import OOV

THEMAP = defaultdict(lambda:OOV)

def set_paths_file(fn):
    """Set the map file for our Brown clusters features."""
    global THEMAP
    THEMAP = defaultdict(lambda:OOV)
    with open(fn) as infile:
        for line in infile:
            cluster, word, count = line.split()
            THEMAP[word] = cluster

def clusters_for_sentence(words):
    """Given a list of words, return the list of clusters for those words."""
    return [THEMAP[w] for w in words]

def main():
    set_paths_file("es-bible-lemmatized-c50-p1.paths")

    print(clusters_for_sentence("en el principio crear dios el cielo y el tierra .".split()))

if __name__ == "__main__": main()
