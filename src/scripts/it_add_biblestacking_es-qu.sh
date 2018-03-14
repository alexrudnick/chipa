#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/bible.es-it.source.annotated \
  --bitext ~/terere/bibletools/output/bible.es-it \
  --alignfn ~/terere/bibletools/output/bible.es-it.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-qu.source.annotated \
  --featureprefix stack_bible_esit

cat PROBLEMS
