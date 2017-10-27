#!/usr/bin/env python3

import argparse
import multiprocessing

from gensim.models import Doc2Vec
import gensim.models.doc2vec
from collections import OrderedDict

import traindoc2vec

SAVED_MODEL = "400-spanish-wikipedia-doc2vec.model"

model = Doc2Vec.load(SAVED_MODEL)

v1 = model.infer_vector('La desalinización es un proceso mediante el cual se elimina la sal del agua de mar o salobre .'.split())
v2 = model.infer_vector('Justin Drew Bieber ( London , Canadá , 1 de marzo de 1994 ) , más conocido como Justin Bieber , es un cantante y compositor canadiense .'.split())
v3 = model.infer_vector('Los requerimientos energéticos de la desalinización varían en función de la tecnología empleada , aunque hay una tendencia hacia su reducción , gracias a los avances tecnológicos .'.split())

print("should be low")
print(traindoc2vec.cosine(v1, v2))

print("should be higher")
print(traindoc2vec.cosine(v1, v3))
