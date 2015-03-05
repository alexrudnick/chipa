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

def window_indices(index, width, length):
    """Return a list of the indices in the window, for width before and after
    the index, constrained by the length of the sequence."""

    lowerbound = max(0, index-width)
    upperbound = min(index+width, length-1)
    indices = list(range(lowerbound, index)) + \
              list(range(index+1, upperbound+1))
    return indices

WIDTH=3
def window(tagged_sent, annotated, index):
    """Immediate surrounding context features."""
    source = nltk.tag.untag(tagged_sent)
    indices = window_indices(index, WIDTH, len(source))
    out = {'w(%s)' % source[i] : True
           for i in indices}
    return out

def clusters_for_sentence(annotated, clusterprefix):
    """Given a list of words, return the list of clusters for those words."""
    clusters = []
    prefix_len = len(clusterprefix)
    out = {}
    for token in annotated:
        cluster = "NONE"
        for annotation in token.annotations:
            if annotation.startswith(clusterprefix):
                cluster = annotation[prefix_len:]
        clusters.append(cluster)
    assert len(clusters) == len(annotated), \
        "clusters: {0} annotated: {1}".format(len(clusters), len(annotated))
    return clusters

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

def brown_variations(featprefix, cluster):
    """Return all the feature variations for this brown cluster."""
    out = {}
    out.update({'%s_complete(%s)' % (featprefix, cluster): True})
    if cluster != "NONE":
        for end in range(0, len(cluster)):
            out.update(dict([('%s_%d(%s)' % (featprefix, end, cluster[:end+1]),
                             True)]))
    return out

def brown_bag_bible(tagged_sent, annotated, index):
    """Bag of all the brown_bible clusters for this sentence."""
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_bible=")
    for cluster in clusters:
        out.update(brown_variations("brown_bag_bible", cluster))
    return out

def brown_window_bible(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_bible=")
    w_indices = window_indices(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_bible", cluster)
        out.update(variations)
    return out

def brown_bag_europarl(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    for cluster in clusters:
        out.update(brown_variations("brown_bag_europarl", cluster))
    return out

def brown_window_europarl(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    w_indices = window_indices(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_europarl", cluster)
        out.update(variations)
    return out

def postag(tagged_sent, annotated, index):
    out = {}
    token = annotated[index]
    for annotation in token.annotations:
        if annotation.startswith("tag="):
            tag = annotation[4:]
            out["postag(%s)" % tag] = True
    return out

def postag_left(tagged_sent, annotated, index):
    out = {}
    if (index - 1) in range(len(annotated)):
        token = annotated[index - 1]
        for annotation in token.annotations:
            if annotation.startswith("tag="):
                tag = annotation[4:]
                out["postag_left(%s)" % tag] = True
    return out

def postag_right(tagged_sent, annotated, index):
    out = {}
    if (index + 1) in range(len(annotated)):
        token = annotated[index + 1]
        for annotation in token.annotations:
            if annotation.startswith("tag="):
                tag = annotation[4:]
                out["postag_right(%s)" % tag] = True
    return out

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
