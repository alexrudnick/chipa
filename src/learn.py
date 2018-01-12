#!/usr/bin/env python3

import argparse
import readline
import functools

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.probability import ConditionalProbDist
from nltk.probability import ELEProbDist

import features
from constants import UNTRANSLATED
from constants import OOV

DEBUG=False
def pause():
    if DEBUG: input("ENTER TO CONTINUE")

def cpd(cfd):
    """Take a ConditionalFreqDist and turn it into a ConditionalProdDist"""
    return ConditionalProbDist(cfd, ELEProbDist)

def reverse_cfd(cfd):
    """Given a ConditionalFreqDist, reverse the conditions and the samples!!"""
    out = ConditionalFreqDist()
    for condition in cfd.conditions():
        for sample in cfd[condition].samples():
            out[sample].inc(condition, cfd[condition][sample])
    return out

@functools.lru_cache(maxsize=100000)
def mfs_for(word):
    fd = nltk.probability.FreqDist()
    labeled_featuresets = trainingdata_for(word)
    for (f,label) in labeled_featuresets:
        fd[label] += 1 
    return fd.max()

@functools.lru_cache(maxsize=100000)
def mfs_translation(word):
    """Return the MFS for the given word, but require that it's not the
    untranslated token unless that's all we've seen."""
    fd = nltk.probability.FreqDist()
    labeled_featuresets = trainingdata_for(word)
    for (f,label) in labeled_featuresets:
        if label == UNTRANSLATED: continue
        fd[label] += 1 
    mostcommon = fd.most_common()
    if not mostcommon:
        return OOV
    return mostcommon[0][0]

class MFSClassifier(nltk.classify.ClassifierI):
    def __init__(self):
        self.fd = nltk.probability.FreqDist()
    def train(self, labeled_featuresets):
        self.fd.clear()
        for (f,label) in labeled_featuresets:
            self.fd[label] += 1 
    def classify(self, featureset):
        return self.fd.max()
    def prob_classify(self, featureset):
        return nltk.probability.DictionaryProbDist({self.fd.max(): 1.0})

class OOVClassifier(nltk.classify.ClassifierI):
    def __init__(self):
        pass
    def train(self, labeled_featuresets):
        pass
    def classify(self, featureset):
        return OOV
    def prob_classify(self, featureset):
        return nltk.probability.DictionaryProbDist({OOV: 1.0})

@functools.lru_cache(maxsize=100000)
def distribution_for(word):
    fd = nltk.probability.FreqDist()
    labeled_featuresets = trainingdata_for(word)
    for (f,label) in labeled_featuresets:
        fd[label] += 1 
    return fd
