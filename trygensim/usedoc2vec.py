#!/usr/bin/env python3

import argparse
import multiprocessing

from gensim.models import Doc2Vec
import gensim.models.doc2vec
from collections import OrderedDict

import trydoc2vec

SAVED_MODEL = "spanish-wikipedia-doc2vec.model"

model = Doc2Vec.load(SAVED_MODEL)

v1 = model.infer_vector('eso es bueno'.split())
v2 = model.infer_vector('eso es perfecto'.split())
v3 = model.infer_vector('eso es malo'.split())

print("should be low")
print(trydoc2vec.cosine(v1, v2))

print("should be higher")
print(trydoc2vec.cosine(v1, v3))
