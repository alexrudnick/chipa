#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/100keuroparl.es-fr.source.annotated \
  --bitext ~/terere/bibletools/output/100keuroparl.es-fr \
  --alignfn ~/terere/bibletools/output/100keuroparl.es-fr.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_default_esfr \

cat PROBLEMS
