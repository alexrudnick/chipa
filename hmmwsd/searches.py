#!/usr/bin/env python3

import itertools
import math
from collections import defaultdict
from collections import namedtuple
from operator import itemgetter

import memm_features
from util_search import build_vocab
import picklestore

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
                ## XXX transition_logprob here too
                emission_penalty = -emissions[newword].logprob(sourceword)
                newpenalty = penalty + transition_penalty + emission_penalty
                newconfigurations.append(Configuration(newseq, newpenalty))

        ## filter down the list of new configurations
        newconfigurations.sort(key=itemgetter(1))
        configurations = newconfigurations[:beamwidth]

    ## now we're done, and we just have to take the best one!
    sequence,penalty = configurations[0]
    return list(zip(unlabeled_sequence, sequence))

def beam_memm(unlabeled_sequence, beamwidth=5):
    classifiers = list(map(picklestore.get, unlabeled_sequence)) ## AWWW YEAH.
    configurations = [Configuration([], 0)]
    T = len(unlabeled_sequence)

    for t in range(T):
        if not configurations: return None
        nones = [None] * (T - t)
        sourceword = unlabeled_sequence[t]

        newconfigurations = []
        for sequence,penalty in configurations:
            seqlabels = sequence + nones
            tagged_sent = list(zip(unlabeled_sequence, seqlabels))
            print(len(tagged_sent), len(seqlabels), len(unlabeled_sequence))
            assert len(tagged_sent) == len(unlabeled_sequence)

            features = memm_features.extract(tagged_sent, t)
            dist = classifiers[t].prob_classify(features)
            probs_and_labels = [(dist.prob(key), key) for key in dist.samples()]

            for (prob,label) in probs_and_labels:
                newseq = sequence + [label]
                ## XXX transition_logprob here too
                newpenalty = penalty + -math.log(prob)
                newconfigurations.append(Configuration(newseq, newpenalty))
        ## filter down the list of new configurations
        newconfigurations.sort(key=itemgetter(1))
        configurations = newconfigurations[:beamwidth]
    ## now we're done, and we just have to take the best one!
    sequence,penalty = configurations[0]
    return list(zip(unlabeled_sequence, sequence))
