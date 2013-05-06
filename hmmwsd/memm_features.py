#!/usr/bin/env python3

"""
Feature detectors here take a tagged sentence of the shape [(s,t)  ...] and
return feature dictionaries.
"""

def bagofwords(tagged_sent):
    """Bag of words features."""
    tokenized = nltk.tag.untag(problem.tagged)
    return dict([('cw(%s)' % w, True) for w in tokenized])

WIDTH=3
def window(tagged_sent):
    """Immediate surrounding context features."""
    tokenized = nltk.tag.untag(problem.tagged)
    out = {}
    for index in problem.head_indices:
        ## window of WIDTH before
        lowerbound = max(0, index-WIDTH)
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[lowerbound:index]])
        out.update(windowfeatures)
        ## and WIDTH after
        upperbound = index+WIDTH
        windowfeatures = dict([('w(%s)' % w, True)
                              for w in tokenized[index+1:upperbound+1]])
        out.update(windowfeatures)
    return out

def extract(tagged_sent):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    allfeatures = [
        bagofwords,
        window,
        prev_label
        prev_two_labels
    ]
    for funk in allfeatures:
        extracted = funk(problem)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out
