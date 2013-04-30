#!/usr/bin/env python3

import itertools
from collections import defaultdict

from util_search import build_vocab
from util_search import transition_logprob

"""
Considering all tags in this kind of setting is a bad idea; there are only maybe
at most tens of tags that are possible for each word. So let's build a new
Viterbi version that takes that into account.
"""

from constants import UNTRANSLATED
from constants import START
from constants import MINCOUNT

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

def viterbi(lm, emissions, cfd, unlabeled_sequence):
    """Takes:
    - the transition probabilities over hidden states as an NgramModel
    - emission probabilities as a ConditionalProbDist
    - a ConditionalFreqDist of the times each hidden state occurred with each
      surface state.
    - the sequence to label.
    """
    T = len(unlabeled_sequence)
    V = { (-1,''):0}
    B = {}
    vocab = build_vocab(unlabeled_sequence, cfd, MINCOUNT=MINCOUNT)

    print("... solving...")
    for t in range(T):
        symbol = unlabeled_sequence[t]
        myvocab = vocab[t]
        pvocab = vocab[t-1]
        for sj in myvocab:
            if sj in emissions.conditions():
                emission_penalty = -emissions[sj].logprob(symbol)
            else:
                emission_penalty = (1000 * 1000)
            best = None
            for si in pvocab:
                context = [si]
                transition_penalty = transition_logprob(lm, sj, context)
                va = V[t-1, si] + transition_penalty + emission_penalty
                if not best or va < best[0]:
                    best = (va, si)
            V[t,sj] = best[0]
            B[t,sj] = best[1]

    ## find the best last state!
    bestend = None
    for si in myvocab:
        context = [si]
        transition_penalty = transition_logprob(lm, '', context)
        penalty = V[T-1, si] + transition_penalty 
        if not bestend or penalty < bestend[0]:
            bestend = (penalty, si)

    labels = [''] * len(unlabeled_sequence)
    labels[T-1] = bestend[1]
    for t in range(T-2, -1, -1):
        labels[t] = B[t+1, labels[t+1]]
    return list(zip(unlabeled_sequence, labels))

def viterbi_trigram(lm, emissions, cfd, unlabeled_sequence):
    """Many thanks to Michael Collins and his great notes on how to do this for
    trigrams."""
    print("sequence:", " ".join(unlabeled_sequence))
    T = len(unlabeled_sequence)
    vocab = build_vocab(unlabeled_sequence, cfd, MINCOUNT=MINCOUNT)

    # the scores, will be indexed by (t, u, v) triples.
    V = { (-1,'',''):0 }
    # the backpointers, will be indexed by (t, u, v) triples.
    B = {}

    print("... solving...")
    for t in range(T):
        symbol = unlabeled_sequence[t]
        myvocab = vocab[t]
        # print(t, symbol, "->", len(myvocab), "different things")
        pvocab = vocab[t-1]
        ppvocab = vocab[t-2]
        for (u,v) in itertools.product(pvocab, myvocab):
            emission_penalty = -emissions[v].logprob(symbol)
            best = None
            for w in ppvocab:
                context = (w,u)
                transition_penalty = transition_logprob(lm, v, context)
                va = V[t-1, w, u] + transition_penalty + emission_penalty
                if not best or va < best[0]:
                    best = (va, w)
            V[t,u,v] = best[0]
            B[t,u,v] = best[1]

    ## find the best pair for the last two!!
    bestend = None
    for (u,v) in itertools.product(pvocab, myvocab):
        context = (u,v)
        transition_penalty = transition_logprob(lm, '', context)
        penalty = V[T-1, u, v] + transition_penalty 
        if not bestend or penalty < bestend[0]:
            bestend = (penalty, context)
    print(bestend)

    labels = [''] * len(unlabeled_sequence)
    labels[T-1] = bestend[1][1]
    labels[T-2] = bestend[1][0]
    ## labels.extend(bestend[1].reversed())
    for t in range(T-3, -1, -1):
        labels[t] = B[t+2, labels[t+1], labels[t+2]]
    return list(zip(unlabeled_sequence, labels))
