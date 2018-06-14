#!/usr/bin/env python3

"""Version of Chipa that speaks fiforpc."""

import os
import functools
import argparse

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.ensemble import RandomForestClassifier

import annotated_corpus
import features
import learn
import list_focus_words
import preprocessing
import trainingdata
import util


SERVER_TO_CLIENT_PATH = "/tmp/server_to_client.fifo"
CLIENT_TO_SERVER_PATH = "/tmp/client_to_server.fifo"

def init_fifos():
    os.remove(SERVER_TO_CLIENT_PATH)
    os.remove(CLIENT_TO_SERVER_PATH)

    if not os.path.exists(SERVER_TO_CLIENT_PATH):
        os.mkfifo(SERVER_TO_CLIENT_PATH)
    if not os.path.exists(CLIENT_TO_SERVER_PATH):
        os.mkfifo(CLIENT_TO_SERVER_PATH)

def send_response(s):
    ## response should be tab-separated and include...
    ## sentence, index, translation, score
    with open(SERVER_TO_CLIENT_PATH, "w") as outfile:
        print(s, file=outfile)

def get_argparser():
    parser = argparse.ArgumentParser(description='chipa_server')
    parser.add_argument('--bitextfn', type=str, required=True)
    parser.add_argument('--alignfn', type=str, required=True)
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--featurefn', type=str, required=True)
    parser.add_argument('--dprint', type=bool, default=False, required=False)
    return parser

@functools.lru_cache(maxsize=100000)
def classifier_for_lemma(lemma):
    # XXX: always doing non-null and Random Forest for initial version
    classifier = SklearnClassifier(RandomForestClassifier(), sparse=False)
    training = trainingdata.trainingdata_for(lemma, nonnull=True)
    print("got {0} instances for {1}".format(len(training), lemma))

    if len(training) > (20 * 1000):
        print("capping to 20k instances to fit in memory")
        training = training[: 20 * 1000]

    labels = set(label for (feat,label) in training)
    print("loaded training data for", lemma)
    if (not training) or len(labels) < 2:
        return None
    classifier.train(training)
    return classifier

def predict_class(classifier, sentence, index):
    """Predict a translation for the token at the current index in this
    annotated sentence."""

    # tags are just the lemma itself
    tagged_sentence = [(tok.lemma, tok.lemma) for tok in sentence]
    # nltk problem instance
    fs, fakelabel = trainingdata.build_instance(tagged_sentence,
                                                sentence,
                                                index)
    return classifier.classify(fs)


def main():
    init_fifos()

    parser = get_argparser()
    args = parser.parse_args()
    util.DPRINT = args.dprint

    featureset_name = os.path.basename(args.featurefn).split('.')[0]
    features.load_featurefile(args.featurefn)
    trainingdata.STOPWORDS = trainingdata.load_stopwords(args.bitextfn)

    ## Setting up training data...
    triple_sentences = trainingdata.load_bitext(args.bitextfn, args.alignfn)
    tl_sentences = trainingdata.get_target_language_sentences(triple_sentences)
    sl_sentences = [s for (s,t,a) in triple_sentences]
    tagged_sentences = [list(zip(ss, ts))
                        for ss,ts in zip(sl_sentences, tl_sentences)]
    trainingdata.set_examples(sl_sentences,tagged_sentences)

    source_annotated = annotated_corpus.load_corpus(args.annotatedfn)
    trainingdata.set_sl_annotated(source_annotated)


    print("OK serving forever.")
    while True:
        line = ""
        with open(CLIENT_TO_SERVER_PATH, "r") as c2s:
            line = c2s.readline()
            line = line.strip()
        print("Received: " + line)
        sentence, index, translation = line.split('\t')
        index = int(index)

        preprocessed = preprocessing.preprocess(sentence, "es", tokenize=False)
        lemma = preprocessed[index].lemma
        print("getting classifier for", lemma)
        classifier = classifier_for_lemma(lemma)

        send_response(line + '\t' + str(len(line)))

if __name__ == "__main__": main()
