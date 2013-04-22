#!/usr/bin/env python3

import itertools
from collections import defaultdict

"""
Considering all tags in this kind of setting is a bad idea; there are only maybe
at most tens of tags that are possible for each word. So let's build a new
Viterbi version that takes that into account.
"""

UNTRANSLATED = "<untranslated>"
START = "***START***"
END = "***END***"

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
            score = cfd['symbol'].logprob(state)
            if score > bestscore:
                bestscore = score
                besttag = state
        out.append((symbol, besttag))
    return out

def maybe_untranslated(samples):
    """Take a list of possibilities and add the untranslated symbol too."""
    return [UNTRANSLATED] + list(samples)

def viterbi(transitions, emissions, cfd, unlabeled_sequence):
    """Viterbi algorithm. Here we're assuming a trigram model, but it should be
    easy-ish to try other widths.
    Takes:
    - the transition probabilities over hidden states as an NgramModel
    - emission probabilities as a ConditionalProbDist
    - a ConditionalFreqDist of the times each hidden state occurred with each
      surface state.
    - the sequence to label.
    """
    print(type(transitions))

    T = len(unlabeled_sequence)
    ## sparse it up!!
    V = defaultdict(float)
    B = {}

    for word in unlabeled_sequence:
        if word not in cfd.conditions():
            cfd[word].inc(UNTRANSLATED)
            ## XXX do we need to do something about emissions? ...

    # find the starting log probabilities for each state
    symbol = unlabeled_sequence[0]
    for sj in cfd[symbol].samples():
        print("sj", sj)
        ## make sure we're always using logprobs
        t = transitions[START,START].logprob(sj)
        e = emissions[sj].logprob(symbol)
        V[0, sj] = t + e
        B[0, sj] = None
    print("V!!\n", V)
    print("B!!\n", B)

    # find the maximum log probabilities for reaching each state at time t
    for t in range(1, T):
        symbol = unlabeled_sequence[t]
        if t-2 < 0:
            pps = [START]
        else:
            pps = cfd[unlabeled_sequence[t-2]].samples()
        ps = cfd[unlabeled_sequence[t-1]].samples()

        for sj in cfd[symbol].samples():
            best = None
            prevstatepairs = itertools.product(pps, ps)
            for si in prevstatepairs:
                print(si)
                va = V[t-1, si] + transitions[si].logprob(sj)
                if not best or va > best[0]:
                    best = (va, si)
            V[t, sj] = best[0] + hmm._output_logprob(sj, symbol)
            B[t, sj] = best[1]

    # find the highest probability final state
    best = None
    for sj in cfd[symbol].samples():
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
