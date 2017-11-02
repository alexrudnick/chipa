#!/usr/bin/env python3

"""
Feature detectors here take a tagged sentence of the shape [(s,t)  ...] and
return feature dictionaries.
"""

from collections import Counter

import nltk
from gensim.models import Doc2Vec
import gensim.models.doc2vec

import word_vectors

DEBUG=False

def NOFEATURES(tagged_sent, annotated, index):
    """An empty dictionary."""
    return dict()

def bagofwords(tagged_sent, annotated, index):
    """Bag of words features."""
    source = nltk.tag.untag(tagged_sent)
    return Counter('cw(%s)' % w for w in source)

def window_indices(index, width, length):
    """Return a list of the indices in the window, for width before and after
    the index, constrained by the length of the sequence."""

    lowerbound = max(0, index-width)
    upperbound = min(index+width, length-1)
    indices = list(range(lowerbound, index)) + \
              list(range(index+1, upperbound+1))
    return indices

def window_indices_inclusive(index, width, length):
    """Return a list of the indices in the window, for width before and after
    the index, constrained by the length of the sequence. Includes index."""

    lowerbound = max(0, index-width)
    upperbound = min(index+width, length-1)
    return list(range(lowerbound, upperbound+1))

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
    return Counter('bs(%s)' % w for w in surface)

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

def surfaceform(tagged_sent, annotated, index):
    """The literal surface form of the focus word."""
    out = {}
    surface = [token.surface for token in annotated]
    return {("surfaceform(%s)" % surface[index]) : True}

def brown_variations(featprefix, cluster):
    """Return all the feature variations for this brown cluster."""
    out = {}
    if cluster == "NONE":
        return out
    out.update({'%s(%s)' % (featprefix, cluster): True})
    ## do prefixes of the complete cluster label at 4, 6, 10, and
    ## the whole cluster (like Turian et al 2010, but they maxed out
    ## at 20. Ours aren't wider than 20 though.)
    for prefixlen in [4, 6, 10]:
        out.update(dict([('%s_%d(%s)' % (featprefix, prefixlen,
                                         cluster[:prefixlen]),
                         True)]))
    return out

def brown_bag_wikipedia(tagged_sent, annotated, index):
    """Bag of all the brown_wikipedia clusters for this sentence."""
    out = Counter()
    clusters = clusters_for_sentence(annotated, "brown_wikipedia=")
    for cluster in clusters:
        variations = brown_variations("brown_bag_wikipedia", cluster)
        for k in variations:
            out.update({k : 1})
    return out

def brown_bag_wikipedia_lemma(tagged_sent, annotated, index):
    """Bag of all the brown_wikipedia_lemma clusters for this sentence."""
    out = Counter()
    clusters = clusters_for_sentence(annotated, "brown_wikipedia_lemma=")
    for cluster in clusters:
        variations = brown_variations("brown_bag_wikipedia_lemma", cluster)
        for k in variations:
            out.update({k : 1})
    return out

def brown_window_wikipedia(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_wikipedia=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_wikipedia", cluster)
        out.update(variations)
    return out

def brown_window_wikipedia_lemma(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_wikipedia_lemma=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_wikipedia_lemma", cluster)
        out.update(variations)
    return out

def brown_bag_europarl(tagged_sent, annotated, index):
    out = Counter()
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    for cluster in clusters:
        variations = brown_variations("brown_bag_europarl", cluster)
        for k in variations:
            out.update({k : 1})
    return out

def brown_window_europarl(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_europarl", cluster)
        out.update(variations)
    return out

def brown_bag_europarl_lemma(tagged_sent, annotated, index):
    out = Counter()
    clusters = clusters_for_sentence(annotated, "brown_europarl_lemma=")
    for cluster in clusters:
        variations = brown_variations("brown_bag_europarl_lemma", cluster)
        for k in variations:
            out.update({k : 1})
    return out

def brown_window_europarl_lemma(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl_lemma=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        variations = brown_variations("brown_window_europarl_lemma", cluster)
        out.update(variations)
    return out

def flat_brown_bag_wikipedia(tagged_sent, annotated, index):
    """Bag of all the brown_wikipedia clusters for this sentence."""
    clusters = clusters_for_sentence(annotated, "brown_wikipedia=")
    return Counter(['fbw(%s)' % c for c in clusters])

def flat_brown_bag_europarl(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    return Counter(['fbe(%s)' % c for c in clusters])

def flat_brown_window_europarl(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_europarl=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        out.update({"fwe(%s)" % cluster: True})
    return out

def flat_brown_window_wikipedia(tagged_sent, annotated, index):
    out = {}
    clusters = clusters_for_sentence(annotated, "brown_wikipedia=")
    w_indices = window_indices_inclusive(index, WIDTH, len(annotated))
    for w_index in w_indices:
        cluster = clusters[w_index]
        out.update({"fww(%s)" % cluster: True})
    return out

def head_lemma(tagged_sent, annotated, index):
    out = {}
    token = annotated[index]
    found = False
    for annotation in token.annotations:
        if annotation.startswith("head_lemma="):
            hl = annotation[len("head_lemma="):]
            out["head_lemma(%s)" % hl] = True
            found = True
    assert found, "couldn't find head_lemma annotation"
    return out

def head_surface(tagged_sent, annotated, index):
    out = {}
    token = annotated[index]
    found = False
    for annotation in token.annotations:
        if annotation.startswith("head_surface="):
            hl = annotation[len("head_surface="):]
            out["head_surface(%s)" % hl] = True
            found = True
    assert found, "couldn't find head_surface annotation"
    return out

def child_lemma(tagged_sent, annotated, index):
    out = {}
    token = annotated[index]
    for annotation in token.annotations:
        if annotation.startswith("child_lemma="):
            hl = annotation[len("child_lemma="):]
            out["child_lemma(%s)" % hl] = True
    return out

def child_surface(tagged_sent, annotated, index):
    out = {}
    token = annotated[index]
    for annotation in token.annotations:
        if annotation.startswith("child_surface="):
            hl = annotation[len("child_surface="):]
            out["child_surface(%s)" % hl] = True
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

### code for word embedding features

EMBEDDINGLOADER=None
EMBEDDINGDIMS=0
def set_embedding_file(fn, ndims):
    global EMBEDDINGLOADER
    EMBEDDINGLOADER = word_vectors.EmbeddingLoader(fn, ndims)

def word2vec_pyramid(tagged_sent, annotated, index):
    assert EMBEDDINGLOADER, "need to specify word embeddings"
    out = {}
    surface = [token.surface for token in annotated]

    word_embeddings = []
    for position,word in enumerate(surface): 
        scaling = (10 - abs(position - index)) / 10
        scaling = max(0, scaling)
        if scaling:
            vec = scaling * EMBEDDINGLOADER.embedding(word)
            word_embeddings.append(vec)
    sent_vector = sum(word_embeddings)
    for i in range(len(sent_vector)):
        out["word2vec_{}".format(i)] = sent_vector[i]
    return out

### end code for word embedding features


### code for document embedding features
DOC2VECMODEL = None

def initialize_doc2vec200():
    global DOC2VECMODEL
    DOC2VECMODEL = Doc2Vec.load(
        "../trygensim/200-spanish-wikipedia-doc2vec.model")

def initialize_doc2vec400():
    global DOC2VECMODEL
    DOC2VECMODEL = Doc2Vec.load(
        "../trygensim/400-spanish-wikipedia-doc2vec.model")

def doc2vec_window_200(tagged_sent, annotated, index):
    if not DOC2VECMODEL:
        initialize_doc2vec200()
    return doc2vec_window("doc2vec_window_200", annotated, index)

def doc2vec_window_400(tagged_sent, annotated, index):
    if not DOC2VECMODEL:
        initialize_doc2vec400()
    return doc2vec_window("doc2vec_window_400", annotated, index)

def doc2vec_window(prefix, annotated, index):
    if not DOC2VECMODEL:
        assert False, "call doc2vec200 or doc2vec400"

    out = {}

    surface = [token.surface for token in annotated]

    lowerbound = max(0, index-WIDTH)
    upperbound = index+WIDTH+1
    surface_window = surface[lowerbound:upperbound]

    sent_vector = DOC2VECMODEL.infer_vector(surface_window)
    for i in range(len(sent_vector)):
        out["{}_{}".format(prefix, i)] = sent_vector[i]
    return out
### end code for document embedding features

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
    """Extract the features for this sentence."""
    out = {}
    allfeatures = [globals()[funkname] for funkname in FEATURES]
    assert(allfeatures), "need some features"
    assert len(tagged_sent) == len(annotated), \
           "length mismatch in tokens vs annotated tokens"
    for funk in allfeatures:
        extracted = funk(tagged_sent, annotated, index)
        if DEBUG: print(funk.__doc__.strip()); print(extracted)
        out.update(extracted)
    return out

def extract_untagged(sentence, annotated, index):
    """Extract the features for this sentence; here sentence is a list of words,
    rather than a list of pairs."""
    tagged_sent = [(word, word) for word in sentence]
    return extract(tagged_sent, annotated, index)
