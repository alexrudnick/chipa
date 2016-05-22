import multiprocessing

from gensim.models import Doc2Vec
import gensim.models.doc2vec
from collections import OrderedDict

CORPUS = "/space/spanish-wikipedia/spanish-wikipedia.txt"
SAVED_MODEL = "spanish-wikipedia-doc2vec.model"

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

    documents = gensim.models.doc2vec.TaggedLineDocument(CORPUS)
    ## XXX: tunable parameter. 100 seems slightly small.
    model = Doc2Vec(documents, size=100, window=8, min_count=1, workers=cores)

    for epoch in range(10):
        print("training step", epoch)
        model.train(documents)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    model.save(SAVED_MODEL)

if __name__ == "__main__": main()
