#!/usr/bin/env python3

"""
Feature detectors here take a tagged sentence of the shape [(s,t)  ...] and
return feature dictionaries.
"""

import nltk

DEBUG=False

def bagofwords(tagged_sent, index):
    """Bag of words features."""
    source = nltk.tag.untag(tagged_sent)
    return dict([('cw(%s)' % w, True) for w in source])

WIDTH=3
def window(tagged_sent, index):
    """Immediate surrounding context features."""
    source = nltk.tag.untag(tagged_sent)
    out = {}
    ## window of WIDTH before
    lowerbound = max(0, index-WIDTH)
    windowfeatures = dict([('w(%s)' % w, True)
                          for w in source[lowerbound:index]])
    out.update(windowfeatures)
    ## and WIDTH after
    upperbound = index+WIDTH
    windowfeatures = dict([('w(%s)' % w, True)
                          for w in source[index+1:upperbound+1]])
    out.update(windowfeatures)
    return out

def getlabel(tagged_sent, i):
    if i in range(len(tagged_sent)):
        return tagged_sent[i][1]
    elif i < 0:
        return "*START*"
    else:
        assert False, "don't ask for the future"

def prev_label(tagged_sent, index):
    out = {}
    out['prevlabel(%s)' % getlabel(tagged_sent, index-1)] = True
    return out

def prev_prev_label(tagged_sent, index):
    out = {}
    out['prevprevlabel(%s)' % getlabel(tagged_sent, index-2)] = True
    return out

def extract(tagged_sent, index):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    allfeatures = [
        bagofwords,
        window,
        #prev_label,
        #prev_prev_label,
    ]
    for funk in allfeatures:
        extracted = funk(tagged_sent, index)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out
