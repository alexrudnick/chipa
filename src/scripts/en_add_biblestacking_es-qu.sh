#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn annotated/bible.es-en.source.annotated \
  --bitext ~/terere/bibletools/output/bible.es-en \
  --alignfn ~/terere/bibletools/output/bible.es-en.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-qu.source.annotated \
  --featureprefix stack_bible_esen

cat PROBLEMS
