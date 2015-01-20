#!/bin/bash

## es-en
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-en \
  --alignfn ~/terere/bibletools/output/bible.es-en.align \
  --featurefn featuresets/default.features \
  --annotatedfn ~/terere/bibletools/output/bible.es-en.source.annotated \
  $@
