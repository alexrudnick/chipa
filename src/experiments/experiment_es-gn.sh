#!/bin/bash

LANGPAIR=es-gn
FEATNAME=$(echo $1 | cut -f 2 -d / | cut -f 1 -d .)

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn annotated/bible.es-gn.source.annotated \
  --featurefn $@ \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
