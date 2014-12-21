#!/usr/bin/env python3

"""
Feature detectors here take a tagged sentence of the shape [(s,t)  ...] and
return feature dictionaries.
"""

import nltk

DEBUG=False

def bagofwords(tagged_sent, annotated, index):
    """Bag of words features."""
    source = nltk.tag.untag(tagged_sent)
    return dict([('cw(%s)' % w, True) for w in source])

WIDTH=3
def window(tagged_sent, annotated, index):
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

def clusters_for_sentence(annotated):
    """Given a list of words, return the list of clusters for those words."""
    clusters = []
    for token in annotated:
        cluster = "brown32=None"
        for annotation in token.annotations:
            if annotation.startswith("brown32="):
                cluster = annotation
        clusters.append(cluster)
    assert len(clusters) == len(annotated), \
        "clusters: {0} annotated: {1}".format(len(clusters), len(annotated))
    return clusters

def bagofbrown(tagged_sent, annotated, index):
    """Bag of brown clusters for the whole sentence."""
    clusters = clusters_for_sentence(annotated)
    return dict([('bb(%s)' % w, True) for w in clusters])

def brownwindow(tagged_sent, annotated, index):
    """Immediate surrounding brown clusters."""
    clusters = clusters_for_sentence(annotated)
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

def bagofsurface(tagged_sent, annotated, index):
    """Bag of words features."""
    surface = [token.surface for token in annotated]
    return dict([('bs(%s)' % w, True) for w in surface])

def surfacewindow(tagged_sent, annotated, index):
    """Immediate surrounding context features from the surface forms."""
    out = {}
    surface = [token.surface for token in annotated]
    ## window of WIDTH before
    lowerbound = max(0, index-WIDTH)
    windowfeatures = dict([('sw(%s)' % w, True)
                          for w in surface[lowerbound:index]])
    out.update(windowfeatures)
    ## and WIDTH after
    upperbound = index+WIDTH
    windowfeatures = dict([('sw(%s)' % w, True)
                          for w in surface[index+1:upperbound+1]])
    out.update(windowfeatures)
    return out

def getlabel(tagged_sent, i):
    if i in range(len(tagged_sent)):
        return tagged_sent[i][1]
    elif i < 0:
        return "*START*"
    else:
        assert False, "don't ask for the future"

FEATURES = []
def load_featurefile(featurefn):
    """Given a filename, load it. Should be one name of a feature function per
    line."""
    names = globals()
    with open(featurefn) as infile:
        for line in infile:
            funkname = line.strip()
            assert funkname in names, \
                "{0} is not a known function".format(funkname)
            FEATURES.append(funkname)

def extract(tagged_sent, annotated, index):
    """Given a WSDProblem, return the features for the sentence."""
    out = {}
    allfeatures = [globals()[funkname] for funkname in FEATURES]
    assert(allfeatures), "need some features"
    for funk in allfeatures:
        extracted = funk(tagged_sent, annotated, index)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out
