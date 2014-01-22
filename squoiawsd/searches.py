#!/usr/bin/env python3

import itertools
import math
from collections import defaultdict
from collections import namedtuple
from operator import itemgetter

from nltk.probability import DictionaryProbDist

from constants import OOV
from constants import UNTRANSLATED
import features

def maxent_mfs(unlabeled_sequence, cfd):
    """If we have a classifier handy, use that. Otherwise, take the MFS."""
    out = []
    #classifiers = list(map(picklestore.get, unlabeled_sequence))
    classifiers = [None for i in unlabeled_sequence]
    ## gotta get a new way to get classifiers...

    T = len(unlabeled_sequence)
    for t in range(0, T):
        symbol = unlabeled_sequence[t]
        if classifiers[t]:
            feat = features.extract(out, t)
            besttag = classifiers[t].classify(feat)
            # print("predicted with maxent:", (symbol, besttag))
            out.append((symbol, besttag))
        else:
            bestscore = float('-inf')
            besttag = UNTRANSLATED
            for state in cfd[symbol].samples():
                score = cfd['symbol'][state]
                if score > bestscore:
                    bestscore = score
                    besttag = state
            out.append((symbol, besttag))
    return out

def mfs(cfd, unlabeled_sequence):
    """Here cfd is the conditional frequency distribution where target-language
    strings are conditioned on source-language ones."""
    out = []
    T = len(unlabeled_sequence)
    for t in range(0, T):
        symbol = unlabeled_sequence[t]
        bestscore = float('-inf')
        besttag = UNTRANSLATED
        for state in cfd[symbol].samples():
            score = cfd['symbol'][state]
            if score > bestscore:
                bestscore = score
                besttag = state
        out.append((symbol, besttag))
    return out

def maybe_untranslated(samples):
    """Take a list of possibilities and add the untranslated symbol too."""
    return [UNTRANSLATED] + list(samples)
