#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/bible.es-nl.source.annotated \
  --bitext ~/terere/bibletools/output/bible.es-nl \
  --alignfn ~/terere/bibletools/output/bible.es-nl.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-qu.source.annotated \
  --featureprefix stack_bible_esnl

cat PROBLEMS
