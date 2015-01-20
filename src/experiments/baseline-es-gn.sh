#!/bin/bash

## es-gn
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --featurefn featuresets/default.features \
  --annotatedfn ~/terere/bibletools/output/bible.es-gn.source.annotated \
  $@
