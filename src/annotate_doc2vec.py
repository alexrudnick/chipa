#!/usr/bin/env python3

"""
Go over an annotated corpus file and add doc2vec annotations for each sentence.

Just put them on the first token in the sentence.
"""
import argparse
from gensim.models import Doc2Vec
import gensim.models.doc2vec

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='annotate_doc2vec')
    parser.add_argument('--annotatedfn', type=str, required=True)
    parser.add_argument('--doc2vecmodel', type=str, required=True)
    parser.add_argument('--featureprefix', type=str, required=True)
    return parser

SAVED_MODEL = None
THEMODEL = None
def getmodel():
    global THEMODEL
    if THEMODEL is None:
        THEMODEL = Doc2Vec.load(SAVED_MODEL)
    return THEMODEL

def get_sentence_vector(sentence):
    """Given a list of tokens, return the sentence vector as a string."""
    model = getmodel()

    surfaces = [token.surface for token in sentence]
    vec = model.infer_vector(surfaces)
    return "_".join(str(x) for x in vec)

def main():
    global SAVED_MODEL
    parser = get_argparser()
    args = parser.parse_args()

    SAVED_MODEL = args.doc2vecmodel
    corpus = annotated_corpus.load_corpus(args.annotatedfn)

    for sentence in corpus:
        first = True
        for token in sentence:
            w = token.surface
            if first:
                sent_embeddingstr = get_sentence_vector(sentence)
                token.annotations.add(args.featureprefix + "=" +
                                      sent_embeddingstr)
                first = False
            print(token)
        print()
        break

if __name__ == "__main__": main()
