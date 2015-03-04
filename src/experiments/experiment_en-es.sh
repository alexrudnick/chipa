#!/bin/bash

## en-es
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.en-es \
  --alignfn ~/terere/bibletools/output/bible.en-es.align \
  --annotatedfn annotated/bible.en-es.source.annotated \
  --featurefn $@
