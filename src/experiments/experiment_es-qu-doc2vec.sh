#!/bin/bash

LANGPAIR=es-qu
FEATNAME=doc2vec

python3 clwsd_experiment_doc2vec.py \
  --bitext ~/terere/bibletools/output/bible.es-qu \
  --alignfn ~/terere/bibletools/output/bible.es-qu.align \
  --annotatedfn annotated/bible.es-qu.source.annotated \
  --featureprefix doc2vec_wikipedia \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
