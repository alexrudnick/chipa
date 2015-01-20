#!/bin/bash

## es-qu
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-qu \
  --alignfn ~/terere/bibletools/output/bible.es-qu.align \
  --featurefn featuresets/default.features \
  --annotatedfn ~/terere/bibletools/output/bible.es-qu.source.annotated \
  $@
