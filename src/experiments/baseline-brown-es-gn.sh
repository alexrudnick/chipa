#!/bin/bash

## es-gn with brown features too
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --featurefn featuresets/default_with_brown.features  \
  --annotatedfn ~/terere/bibletools/output/bible.es-gn.source.annotated \
  $@
