#!/bin/bash

## es-en
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/bible.es-en \
  --alignfn ~/terere/bibletools/bible.es-en.align \
  --featurefn featuresets/default.features \
  --surfacefn ~/terere/bibletools/bible.es-en.surface
