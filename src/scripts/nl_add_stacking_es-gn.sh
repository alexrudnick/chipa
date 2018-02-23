#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/europarl.es-nl.source.annotated \
  --bitext ~/terere/bibletools/output/europarl.es-nl \
  --alignfn ~/terere/bibletools/output/europarl.es-nl.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_default_esnl \

cat PROBLEMS
