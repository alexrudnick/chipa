#!/usr/bin/env python3

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
            print(symbol, state, score)
            if score > bestscore:
                bestscore = score
                besttag = state
        out.append((symbol, besttag))
    return out

def viterbi(hmm, cfd, unlabeled_sequence):
    """This needs to get built, huh."""

    raise NotImplementedError

    T = len(unlabeled_sequence)
    N = len(hmm._states)
    V = np.zeros((T, N), np.float64)
    B = {}

    # find the starting log probabilities for each state
    symbol = unlabeled_sequence[0]
    for i, state in enumerate(hmm._states):
        V[0, i] = hmm._priors.logprob(state) + \
                  hmm._output_logprob(state, symbol)
        B[0, state] = None

    # find the maximum log probabilities for reaching each state at time t
    for t in range(1, T):
        symbol = unlabeled_sequence[t]
        for j in range(N):
            sj = hmm._states[j]
            best = None
            for i in range(N):
                si = hmm._states[i]
                va = V[t-1, i] + hmm._transitions[si].logprob(sj)
                if not best or va > best[0]:
                    best = (va, si)
            V[t, j] = best[0] + hmm._output_logprob(sj, symbol)
            B[t, sj] = best[1]

    # find the highest probability final state
    best = None
    for i in range(N):
        val = V[T-1, i]
        if not best or val > best[0]:
            best = (val, hmm._states[i])

    # traverse the back-pointers B to find the state sequence
    current = best[1]
    sequence = [current]
    for t in range(T-1, 0, -1):
        last = B[t, current]
        sequence.append(last)
        current = last

    sequence.reverse()
    return sequence
