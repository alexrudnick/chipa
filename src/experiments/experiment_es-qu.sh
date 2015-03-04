#!/bin/bash

## es-qu
python3 clwsd_experiment.py \
  --bitext ~/terere/bibletools/output/bible.es-qu \
  --alignfn ~/terere/bibletools/output/bible.es-qu.align \
  --annotatedfn annotated/bible.es-qu.source.annotated \
  --featurefn $@
