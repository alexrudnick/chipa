#!/usr/bin/env python3

"""
Script for running in-vitro CL-WSD experiments with cross-validation, given
some aligned bitext and quickly moving things into embedding space.

Plan for this is going to look like...

Simple version:
- sum up the word vectors for the whole sentence, that's your features. done.
  "continuous bag-of-words" features for the sentence.
slightly more nuanced:
- sum up the vectors for the window around the focus word.
- alternatively: sum up the vectors for the whole sentence, but discount the
  vectors as they get farther away from the focus word.
"""

from collections import defaultdict
from operator import itemgetter
import argparse
import os
import sys

import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import accuracy_score

import annotated_corpus
import features
import learn
import trainingdata
import word_vectors
import util

def count_correct(classifier, testdata):
    """Given an NLTK-style classifier and some test data, count how many of the
    test instances this classifier gets correct."""
    results = [classifier.classify(fs) for (fs,l) in testdata]
    correct = [l==r for ((fs,l), r) in zip(testdata, results)]
    return correct.count(True)

EMBEDDINGS=None
EMBEDDING_DIM=None
@util.timeexecution
def cross_validate(classifier, top_words, nonnull=False):
    """Given the most common words in the Spanish corpus, cross-validate our
    classifiers for each of those."""
    ## return a map from word to [(ncorrect,size)]
    out = defaultdict(list)
    util.dprint("cross validating this many words:", len(top_words))

    loader = word_vectors.EmbeddingLoader(EMBEDDINGS, EMBEDDING_DIM)

    for w in top_words:
        util.dprint("cross validating:", w)
        text_with_labels = trainingdata.text_label_pairs(w, nonnull=nonnull)

        training = []
        for text, label in text_with_labels:
            word_embeddings = [loader.embedding(word) for word in text]
            sent_vector = sum(word_embeddings)
            training.append((sent_vector, label))
        print("this many instances for {0}: {1}".format(w, len(training)))
        labels = set(label for (feat,label) in training)

        if len(labels) < 2:
            continue
        if len(training) < 10:
            print("not enough samples for", w)
            continue
        ## using constant random_state of 0 for reproducibility
        cv = cross_validation.KFold(len(training), n_folds=10,
                                    shuffle=False, random_state=0)
        for traincv, testcv in cv:
            mytraining = [training[i] for i in traincv]
            mytesting = [training[i] for i in testcv]

            mytraining_X = [x for (x, y) in mytraining]
            mytraining_Y = [y for (x, y) in mytraining]
            classifier.fit(mytraining_X, mytraining_Y) 
            print("trained!!", classifier)

            mytesting_X = [x for (x, y) in mytesting]
            mytesting_Y = [y for (x, y) in mytesting]
            predicted = classifier.predict(mytesting_X)
            ncorrect = sum(int(real == pred) for real, pred
                           in zip(mytesting_Y, predicted))
            out[w].append((ncorrect,len(mytesting)))
    return out

def words_with_differences(results_table):
    """get the words with the biggest classifier vs mfs differences"""
    ## these are going to be the proportion of the cases that classifiers win
    ## over mfs.
    word_diff_pairs = []
    for w, resultslist in results_table.items():
        totalcorrect = sum(correct for (correct,y,z) in resultslist)
        totalmfscorrect = sum(correct for (x,mfscorrect,z) in resultslist)
        totalsize = sum(correct for (x,z,size) in resultslist)
        word_diff_pairs.append((word,
                               (totalcorrect - totalmfscorrect) / totalsize))
    words_with_differences.sort(key=itemgetter(1), reverse=True)
    for word, diff in words_with_differences:
        print("{0}\t{1}".format(word,diff))

## @util.timeexecution
def do_a_case(classifier, top_words, nonnull, casename, stamp):
    print("[[next case]]", casename)
    sys.stdout.flush()
    with open("results/{0}-{1}".format(stamp, casename), "w") as outfile:
        results_table = cross_validate(classifier, top_words, nonnull=nonnull)
        ## one entry into these per word
        corrects = []
        mfscorrects = []
        sizes = []
        for w, resultslist in results_table.items():
            for (correct,size) in resultslist:
                corrects.append(correct)
                sizes.append(size)
        avg = sum(corrects) / sum(sizes)
        print("accuracy: {0:.4f}".format(avg), file=outfile)

def get_argparser():
    parser = argparse.ArgumentParser(description='clwsd_experiment')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    parser.add_argument('--embeddings', type=str, default=False, required=True)
    parser.add_argument('--embedding_dim', type=int, default=False, required=True)
    return parser

def load_top_words():
    out = []
    # XXX: make this a parameter
    with open("focus_words/es-gn") as infile:
        for line in infile:
            out.append(line.strip())
    return out

def main():
    global EMBEDDINGS
    global EMBEDDING_DIM
    parser = get_argparser()
    args = parser.parse_args()


    EMBEDDINGS = args.embeddings
    EMBEDDING_DIM = args.embedding_dim

    util.DPRINT = args.dprint
    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    print("## RUNNING EXPERIMENT on {0} with features {1}".format(
        os.path.basename(args.bitextfn), "EMBEDDINGS"))

    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences, tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)
    top_words = load_top_words()

    ## default is 1e-4.
    THETOL = 1e-4
    classifier_pairs = []
    ## classifier = SklearnClassifier(LogisticRegression(C=1,
    ##                                penalty='l1',
    ##                                tol=THETOL))
    classifier = LogisticRegression(C=1, penalty='l1', tol=THETOL)
    classifier_pairs.append(("maxent-l1-c1", classifier))
    language_pair = args.bitextfn.split(".")[1]
    stamp = util.timestamp() + "-" + language_pair
    featureset_name = "word2vec_" + os.path.basename(args.embeddings)

    for (clname, classifier) in classifier_pairs:
        casename = "{0}-{1}-regular".format(clname, featureset_name)
        do_a_case(classifier, top_words, False, casename, stamp)
        # casename = "{0}-{1}-nonnull".format(clname, featureset_name)
        # do_a_case(classifier, top_words, True, casename, stamp)

if __name__ == "__main__": main()
