#!/usr/bin/env python3

import itertools
from collections import defaultdict
from collections import namedtuple
from operator import itemgetter

from util_search import build_vocab

Configuration = namedtuple('Configuration', ['sequence', 'penalty'])

def astar(lm, emissions, cfd, unlabeled_sequence):
    """Best-first search stack decoder. Do it."""
    ## MINCOUNT = 5
    vocab = build_vocab(unlabeled_sequence, cfd, 5)
    configurations = [Configuration([], 0)]

    while True:
        if not configurations: return None
        configurations.sort(key=itemgetter(1), reverse=True)
        if len(configurations) % 1000 == 0:
            print(len(configurations), "configurations under consideration")
        sequence, penalty = configurations.pop()
        ## print(sequence, penalty)

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
def beam(lm, emissions, cfd, unlabeled_sequence, beamwidth=5):
    vocab = build_vocab(unlabeled_sequence, cfd, 5)
    configurations = [Configuration([], 0)]
    T = len(unlabeled_sequence)

    for t in range(T):
        if not configurations: return None
        sourceword = unlabeled_sequence[t]

        ## pseudocodes.
        newconfigurations = []
        for sequence,penalty in configurations:
            ##for each possible new word:
            ##    create a new configuration where we add that word to that old
            ##    configuration
            ##    add new configuration to list of new configurations
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
                newconfigurations.append(Configuration(newseq, newpenalty))

        ## filter down the list of new configurations
        newconfigurations.sort(key=itemgetter(1))
        configurations = newconfigurations[:beamwidth]

    ## now we're done, and we just have to take the best one!
    sequence,penalty = configurations[0]
    return list(zip(unlabeled_sequence, sequence))
