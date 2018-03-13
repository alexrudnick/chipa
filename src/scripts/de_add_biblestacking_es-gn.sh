#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/bible.es-de.source.annotated \
  --bitext ~/terere/bibletools/output/bible.es-de \
  --alignfn ~/terere/bibletools/output/bible.es-de.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_bible_esde

cat PROBLEMS
