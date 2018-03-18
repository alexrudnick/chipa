#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/europarl.es-fr.source.annotated \
  --bitext ~/terere/bibletools/output/europarl.es-fr \
  --alignfn ~/terere/bibletools/output/europarl.es-fr.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-qu.source.annotated \
  --featureprefix stack_default_esfr \

cat PROBLEMS
