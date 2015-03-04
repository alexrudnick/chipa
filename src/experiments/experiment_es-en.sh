#!/bin/bash

LANGPAIR=es-en
FEATNAME=$(echo $1 | cut -f 2 -d / | cut -f 1 -d .)

python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-en \
  --alignfn ~/terere/bibletools/output/bible.es-en.align \
  --annotatedfn annotated/bible.es-en.source.annotated \
  --featurefn $@ \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
