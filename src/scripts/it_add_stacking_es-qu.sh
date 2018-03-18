#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/europarl.es-it.source.annotated \
  --bitext ~/terere/bibletools/output/europarl.es-it \
  --alignfn ~/terere/bibletools/output/europarl.es-it.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-qu.source.annotated \
  --featureprefix stack_default_esit \

cat PROBLEMS
