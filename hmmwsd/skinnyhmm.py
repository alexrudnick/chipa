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

UNTRANSLATED = "<untranslated>"
START = ""
MINCOUNT = 5

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

def wrongviterbi(lm, emissions, cfd, unlabeled_sequence):
    """Viterbi algorithm. Here we're assuming a trigram model, but it should be
    easy-ish to try other widths.
    Takes:
    - the transition probabilities over hidden states as an NgramModel
    - emission probabilities as a ConditionalProbDist
    - a ConditionalFreqDist of the times each hidden state occurred with each
      surface state.
    - the sequence to label.
    """
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
        ## make sure we're always using logprobs and they always return negative
        ## logprobs, ie, positive penalties.
        t = lm.logprob(sj, [])
        e = -emissions[sj].logprob(symbol)
        V[0, sj] = t + e
        B[0, sj] = None

    # find the maximum log probabilities for reaching each state at time t
    for t in range(1, T):
        symbol = unlabeled_sequence[t]
        if t-2 < 0:
            pps = [START]
        else:
            pps = list(cfd[unlabeled_sequence[t-2]].samples()) or [UNTRANSLATED]
        ps = list(cfd[unlabeled_sequence[t-1]].samples()) or [UNTRANSLATED]

        for sj in cfd[symbol].samples():
            best = None
            emission_penalty = -emissions[sj].logprob(symbol)
            prevstatepairs = list(itertools.product(pps, ps))
            for si in prevstatepairs:
                context = si
                transition_penalty = transition_logprob(lm, sj, context)
                va = V[t-1, si] + transition_penalty + emission_penalty
                if not best or va < best[0]:
                    best = (va, si)
            V[t, sj] = best[0] + -emissions[sj].logprob(symbol)
            ## XXX maybe we could write it down here?
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
    ## XXX overlapping windows of tags...
    for t in range(T-1, 0, -1):
        last = B[t, current]
        print("LAST", last)
        last = last[-1]
        sequence.append(last)
        current = last
    sequence.reverse()
    return list(zip(unlabeled_sequence, sequence))

def viterbi(lm, emissions, cfd, unlabeled_sequence):
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
