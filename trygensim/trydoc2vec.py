import multiprocessing

from gensim.models import Doc2Vec
import gensim.models.doc2vec
from collections import OrderedDict


def magnitude(vec):
    import math
    return math.sqrt(sum((vi * vi) for vi in vec))

def cosine(vec1, vec2):
    assert len(vec1) == len(vec2), "vectors need to be same length"
    ## dotproduct
    top = sum(x1 * x2 for (x1,x2) in zip(vec1, vec2))
    ## ... divided by product of magnitudes
    return top / (magnitude(vec1) * magnitude(vec2))

cores = multiprocessing.cpu_count()
assert gensim.models.doc2vec.FAST_VERSION > -1, "this will be painfully slow"

documents = gensim.models.doc2vec.TaggedLineDocument("europarl-es-10k.txt")

## xxx: need some size more like 100
model = Doc2Vec(documents, size=10, window=8, min_count=1, workers=cores)

inferred = model.infer_vector("Esta directiva trata más concretamente sobre la materia prima que sobre aditivos.".split())
print(inferred)

for epoch in range(10):
    print("training step", epoch)
    model.train(documents)
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

print("now we have trained")
inferred1 = model.infer_vector("Esta directiva trata más concretamente sobre la materia prima que sobre aditivos.".split())
print(inferred1)
print("one versus one:", cosine(inferred1, inferred1))

inferred2 = model.infer_vector("Esta ley trata más concretamente sobre la materia prima que sobre aditivos.".split())
print(inferred2)
print("one versus two:", cosine(inferred1, inferred2))

inferred3 = model.infer_vector("Estas leyes tratan más concretamente sobre la materia prima que sobre aditivos.".split())
print(inferred3)
print("one versus three:", cosine(inferred1, inferred3))
print("two versus three:", cosine(inferred2, inferred3))


inferred4 = model.infer_vector("La votación tendrá lugar mañana a las 11.30 horas.")
print(inferred4)
print("one versus four:", cosine(inferred1, inferred4))
