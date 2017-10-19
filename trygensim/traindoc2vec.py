#!/usr/bin/env python3

import argparse
import multiprocessing

from gensim.models import Doc2Vec
import gensim.models.doc2vec
from collections import OrderedDict

CORPUS = "eswiki.twentymillion.sentences"
SAVED_MODEL = "200-spanish-wikipedia-doc2vec.model"

TINYCORPUS = "europarl-es-10k.txt"
TINY_SAVED_MODEL = "europarl-es-10k-doc2vec.model"

def get_argparser():
    parser = argparse.ArgumentParser(description='trydoc2vec')
    parser.add_argument('--tiny', type=bool, default=False, required=False)
    return parser

def magnitude(vec):
    import math
    return math.sqrt(sum((vi * vi) for vi in vec))

def cosine(vec1, vec2):
    assert len(vec1) == len(vec2), "vectors need to be same length"
    ## dotproduct
    top = sum(x1 * x2 for (x1,x2) in zip(vec1, vec2))
    ## ... divided by product of magnitudes
    return top / (magnitude(vec1) * magnitude(vec2))

def main():
    cores = multiprocessing.cpu_count()
    assert gensim.models.doc2vec.FAST_VERSION > -1, "need fast version"

    parser = get_argparser()
    args = parser.parse_args()

    thecorpus = CORPUS
    savedmodel = SAVED_MODEL
    if args.tiny:
        thecorpus = TINYCORPUS
        savedmodel = TINY_SAVED_MODEL

    documents = gensim.models.doc2vec.TaggedLineDocument(thecorpus)
    print("built the documents object!")

    model = Doc2Vec(documents, size=200, window=8, min_count=5,
                    max_vocab_size=(160 * 1000), workers=cores)
    print("built the model object!")

    print("now training!")
    model.train(documents,
                epochs=model.iter,
                total_examples=model.corpus_count)
    model.save(savedmodel)
    print("done!")

if __name__ == "__main__": main()
