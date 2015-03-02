#!/bin/bash

## es-en with brown features too
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-en \
  --alignfn ~/terere/bibletools/output/bible.es-en.align \
  --featurefn featuresets/default_with_brown.features  \
  --annotatedfn annotated/bible.es-en.source.annotated \
  $@
