#!/usr/bin/env python3

from operator import itemgetter

def get_gold_answers(sourceword, target):
    """Given a source word and a target language, load up the gold answers for
    that word and return a map from problem ids to the best answer for that
    instance."""
    out = {}
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
                word_count_pairs.append((word,int(count)))
            maxpair = max(word_count_pairs, key=itemgetter(1))
            out[problemid] = maxpair[0]
    return out
