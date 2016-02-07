#!/usr/bin/env python3

"""
Go over a Brown cluster file and get the top N words by count for each cluster.
"""

import sys
from collections import Counter
from collections import defaultdict

N = 20
def main():
    clusterfn = sys.argv[1]
    counters = defaultdict(Counter)

    with open(clusterfn) as infile:
        for line in infile:
            cluster, word, count = line.strip().split('\t')
            count = int(count)
            counters[cluster][word] = count

    for cluster in sorted(counters.keys()):
        topwords = [word for word, count in counters[cluster].most_common(N)]
        print(cluster, " ".join(topwords))

if __name__ == "__main__": main()
