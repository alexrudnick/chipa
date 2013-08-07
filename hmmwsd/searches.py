#!/usr/bin/env python3

import itertools
import math
from collections import defaultdict
from collections import namedtuple
from operator import itemgetter

from nltk.probability import DictionaryProbDist

from constants import OOV
from util_search import build_vocab
from util_search import transition_logprob
import memm_features
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
                transition_penalty = transition_logprob(lm, newword, context)
                try:
                    emission_penalty = -emissions[newword].logprob(sourceword)
                except:
                    ## XXX: this should probably have its own function.
                    emission_penalty = (1000*1000)
                newpenalty = penalty + transition_penalty + emission_penalty
                newconfigurations.append(Configuration(newseq, newpenalty))

        ## filter down the list of new configurations
        newconfigurations.sort(key=itemgetter(1))
        configurations = newconfigurations[:beamwidth]

    ## now we're done, and we just have to take the best one!
    sequence,penalty = configurations[0]
    return list(zip(unlabeled_sequence, sequence))


## XXX what do we need for this one?
## - hmm parts
## - current sequence.
## - timestep
def backoff_conditional_distribution(tagged_sent, t, vocab, hmmparts):
    """We don't have a classifier stored for this word. So we want to compute
    this distribution here:

    P(label | word, prevlabel) = \
        P(label|prevlabel) * P(word|label,prevlabel) / P(word)

    ... as negative logprobs, of course. P(word|label, prevlabel) we approximate
    as just P(word|label).
    """
    if OOV in vocab[t]:
        return [(OOV, 1.0)]
    out = []
    sw = tagged_sent[t][0]
    context = ['','']
    if t > 0: context[1] = tagged_sent[t-1][1]
    if t > 1: context[0] = tagged_sent[t-2][1]
    for newword in vocab[t]:
        transition_penalty = transition_logprob(hmmparts.lm, newword, context)
        emission_penalty = -hmmparts.emissions[newword].logprob(sw)
        newpenalty = transition_penalty + emission_penalty
        out.append((newword, newpenalty))
    return out

def beam_memm(unlabeled_sequence, hmmparts, beamwidth=5):
    """Do a beam search for the best sequence labels for the given unlabeled
    sequence using MEMMs!"""

    vocab = build_vocab(unlabeled_sequence, hmmparts.cfd, 5)
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
            assert len(tagged_sent) == len(unlabeled_sequence)

            if classifiers[t]:
                # print(unlabeled_sequence[t], "-> classifier.")
                features = memm_features.extract(tagged_sent, t)
                dist = classifiers[t].prob_classify(features)
                probs_and_labels = [(dist.prob(key), key) for key in dist.samples()]
                for (prob,label) in probs_and_labels:
                    newseq = sequence + [label]
                    newpenalty = penalty + -math.log(prob)
                    newconfigurations.append(Configuration(newseq, newpenalty))
            else:
                # print(unlabeled_sequence[t], "-> back off to hmm.")
                pairs = backoff_conditional_distribution(tagged_sent, t,
                                                         vocab, hmmparts)
                for (label, transpenalty) in pairs:
                    newseq = sequence + [label]
                    newpenalty = penalty + transpenalty
                    newconfigurations.append(Configuration(newseq, newpenalty))
        ## filter down the list of new configurations
        newconfigurations.sort(key=itemgetter(1))
        configurations = newconfigurations[:beamwidth]
    ## now we're done, and we just have to take the best one!
    sequence,penalty = configurations[0]
    return list(zip(unlabeled_sequence, sequence))
