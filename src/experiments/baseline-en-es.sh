#!/bin/bash

## en-es
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.en-es \
  --alignfn ~/terere/bibletools/output/bible.en-es.align \
  --featurefn featuresets/default.features \
  --annotatedfn ~/terere/bibletools/output/bible.en-es.source.annotated \
  $@
