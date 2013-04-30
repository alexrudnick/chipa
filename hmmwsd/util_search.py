#!/usr/bin/env python3

from constants import UNTRANSLATED
from util_run_experiment import final_test_words
import read_gold

preset_dictionary = {}
def init_preset_dictionary(targetlang):
    count = 0
    for sourceword in final_test_words:
        preset_dictionary[sourceword] = \
            read_gold.get_possible_senses(sourceword, targetlang)
        count += 1
    print("OK, initialized dictionary for {0} words.".format(count))

def build_vocab(unlabeled_sequence, cfd, MINCOUNT):
    T = len(unlabeled_sequence)
    vocab = {}
    vocab[-2] = ['']
    vocab[-1] = ['']
    for t in range(T):
        symbol = unlabeled_sequence[t]
        # labels = set(cfd[symbol].samples()) - set(cfd[symbol].hapaxes())
        thevocab = []
        if symbol in preset_dictionary:
            thevocab = list(preset_dictionary[symbol])
        else:
            for (label, count) in cfd[symbol].items():
                if count >= MINCOUNT:
                    thevocab.append(label)
                else:
                    ## they're guaranteed to come out in sorted order.
                    break
        vocab[t] = thevocab
        if UNTRANSLATED in thevocab:
            print(symbol, thevocab)
            print(cfd[symbol].items())
            assert False
        if not vocab[t]:
            vocab[t] = ["<untranslated>"]
    return vocab

def transition_logprob(lm, state, context):
    """... make sure we don't accidentally take the log of 0."""
    transition_prob = lm.prob(state, context)
    transition_penalty = (lm.logprob(state, context) if transition_prob
                                                     else (1000*1000))
    return transition_penalty
