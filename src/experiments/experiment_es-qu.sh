#!/bin/bash

LANGPAIR=es-qu
FEATNAME=$(echo $1 | cut -f 2 -d / | cut -f 1 -d .)

python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-qu \
  --alignfn ~/terere/bibletools/output/bible.es-qu.align \
  --annotatedfn annotated/bible.es-qu.source.annotated \
  --featurefn $@ \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
