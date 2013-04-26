#!/usr/bin/env python3

import itertools
from collections import defaultdict
from collections import namedtuple
from operator import itemgetter

Configuration = namedtuple('Configuration', ['sequence', 'penalty'])

def build_vocab(unlabeled_sequence, cfd, MINCOUNT):
    T = len(unlabeled_sequence)
    vocab = {}
    vocab[-2] = ['']
    vocab[-1] = ['']
    for t in range(T):
        symbol = unlabeled_sequence[t]
        # labels = set(cfd[symbol].samples()) - set(cfd[symbol].hapaxes())
        thevocab = []
        for (label, count) in cfd[symbol].items():
            if count >= MINCOUNT:
                thevocab.append(label)
            else: break
        vocab[t] = thevocab
        if not vocab[t]:
            vocab[t] = ["<untranslated>"]
    return vocab

def astar(lm, emissions, cfd, unlabeled_sequence):
    """Best-first search stack decoder. Do it."""
    ## MINCOUNT = 5
    vocab = build_vocab(unlabeled_sequence, cfd, 5)
    configurations = [Configuration([], 0)]

    while True:
        if not configurations: return None
        configurations.sort(key=itemgetter(1), reverse=True)
        print(len(configurations), "configurations under consideration")
        sequence, penalty = configurations.pop()
        print(sequence, penalty)

        if len(sequence) == len(unlabeled_sequence):
            return list(zip(unlabeled_sequence, sequence))

        t = len(sequence)
        sourceword = unlabeled_sequence[t]
        context = sequence[-2:]
        if not context:
            context = ['', '']
        elif len(context) == 1:
            context = [''] + context

        for newword in vocab[t]:
            newseq = sequence + [newword]
            transition_prob = lm.prob(newword, context)
            transition_penalty = (lm.logprob(newword, context)
                                  if transition_prob else (1000*1000))
            emission_penalty = -emissions[newword].logprob(sourceword)
            newpenalty = penalty + transition_penalty + emission_penalty
            configurations.append(Configuration(newseq, newpenalty))

## do a beam search. do it.
def beam(lm, emissions, cfd, unlabeled_sequence):
    raise NotImplementedError("beam")
