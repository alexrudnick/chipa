#!/usr/bin/env python3

from collections import defaultdict

"""
Considering all tags in this kind of setting is a bad idea; there are only maybe
at most tens of tags that are possible for each word. So let's build a new
Viterbi version that takes that into account.
"""

def mfs(hmm, cfd, unlabeled_sequence):
    out = []
    # find the maximum log probabilities for reaching each state at time t
    T = len(unlabeled_sequence)
    for t in range(0, T):
        symbol = unlabeled_sequence[t]
        bestscore = float('-inf')
        besttag = "<untranslated>"
        ## XXX: this is ridiculous, don't try all possible states.
        for state in cfd[symbol].samples():
            score = hmm._output_logprob(state, symbol)
            if score > bestscore:
                bestscore = score
                besttag = state
        out.append((symbol, besttag))
    return out

def maybe_untranslated(samples):
    """Take a list of possibilities and add the untranslated symbol too."""
    return ["<untranslated>"] + list(samples)

def viterbi(hmm, cfd, unlabeled_sequence):
    """Viterbi algorithm, based on the simple one from NLTK, but requires the
    ConditionalFreqDist over the events of source words being translated as
    target phrases. Sensibly fast for large tag sets."""

    T = len(unlabeled_sequence)
    ## sparse it up!!
    V = defaultdict(float)
    B = {}

    # find the starting log probabilities for each state
    symbol = unlabeled_sequence[0]
    for sj in maybe_untranslated(cfd[symbol].samples()):
        V[0, sj] = hmm._priors.logprob(sj) + \
                   hmm._output_logprob(sj, symbol)
        B[0, sj] = None

    # find the maximum log probabilities for reaching each state at time t
    for t in range(1, T):
        symbol = unlabeled_sequence[t]
        prevsymbol = unlabeled_sequence[t-1]
        for sj in maybe_untranslated(cfd[symbol].samples()):
            best = None
            for si in maybe_untranslated(cfd[prevsymbol].samples()):
                va = V[t-1, si] + hmm._transitions[si].logprob(sj)
                if not best or va > best[0]:
                    best = (va, si)
            V[t, sj] = best[0] + hmm._output_logprob(sj, symbol)
            B[t, sj] = best[1]

    # find the highest probability final state
    best = None
    for sj in maybe_untranslated(cfd[symbol].samples()):
        val = V[T-1, sj]
        if not best or val > best[0]:
            best = (val, sj)

    # traverse the back-pointers B to find the state sequence
    current = best[1]
    sequence = [current]
    for t in range(T-1, 0, -1):
        last = B[t, current]
        sequence.append(last)
        current = last
    sequence.reverse()
    return list(zip(unlabeled_sequence, sequence))
