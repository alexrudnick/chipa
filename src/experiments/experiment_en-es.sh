#!/bin/bash

LANGPAIR=en-es
FEATNAME=$(echo $1 | cut -f 2 -d / | cut -f 1 -d .)

python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.en-es \
  --alignfn ~/terere/bibletools/output/bible.en-es.align \
  --annotatedfn annotated/bible.en-es.source.annotated \
  --featurefn $@ \
  | tee LOGS/log_"$LANGPAIR"_"$FEATNAME"
