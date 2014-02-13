#!/usr/bin/env python3

"""
Feature detectors here take a tagged sentence of the shape [(s,t)  ...] and
return feature dictionaries.
"""

import nltk

import brownclusters
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

def bagofbrown(tagged_sent, index):
    """Bag of brown clusters for the whole sentence."""
    source = nltk.tag.untag(tagged_sent)
    clusters = brownclusters.clusters_for_sentence(source)
    return dict([('bb(%s)' % w, True) for w in clusters])

def brownwindow(tagged_sent, index):
    """Immediate surrounding brown clusters."""
    source = nltk.tag.untag(tagged_sent)
    clusters = brownclusters.clusters_for_sentence(source)
    out = {}
    ## window of WIDTH before
    lowerbound = max(0, index-WIDTH)
    windowfeatures = dict([('bw(%s)' % w, True)
                          for w in clusters[lowerbound:index]])
    out.update(windowfeatures)
    ## and WIDTH after
    upperbound = index+WIDTH
    windowfeatures = dict([('bw(%s)' % w, True)
                          for w in clusters[index+1:upperbound+1]])
    out.update(windowfeatures)
    return out

def getlabel(tagged_sent, i):
    if i in range(len(tagged_sent)):
        return tagged_sent[i][1]
    elif i < 0:
        return "*START*"
    else:
        assert False, "don't ask for the future"

def extract(tagged_sent, index):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    allfeatures = [
        bagofwords,
        window,
        bagofbrown,
        brownwindow,
    ]
    for funk in allfeatures:
        extracted = funk(tagged_sent, index)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out
