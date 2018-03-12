#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/bible.es-fr.source.annotated \
  --bitext ~/terere/bibletools/output/bible.es-fr \
  --alignfn ~/terere/bibletools/output/bible.es-fr.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_bible_esfr

cat PROBLEMS
