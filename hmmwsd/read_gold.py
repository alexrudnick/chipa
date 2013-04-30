#!/usr/bin/env python3

from operator import itemgetter

def get_possible_senses(sourceword, target):
    """Given a source word and a target language, load up the gold answers for
    that word and return a set of the target-language translations (sense
    labels) for that source word."""
    out = set()
    fn = "../eval/{0}.gold.{1}".format(sourceword, target)
    with open(fn) as infile:
        for line in infile:
            splitted = line.split(None, 3)
            problemid = splitted[1]
            rest = splitted[3].strip()
            assert rest.endswith(';')
            rest = rest[:-1]

            word_count_pairs = []
            for wordandcount in rest.split(';'):
                word, count = wordandcount.rsplit(None, 1) # count is rightmost
                word = word.lower()
                out.add(word)
    return out
