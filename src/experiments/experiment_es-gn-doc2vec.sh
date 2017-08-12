#!/bin/bash

LANGPAIR=es-gn
FEATNAME=doc2vec

python3 clwsd_experiment_doc2vec.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn annotated/bible.es-gn.source.annotated \
  --featureprefix doc2vec_wikipedia \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
