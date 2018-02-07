#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/europarl.es-en.source.annotated \
  --bitext ~/terere/bibletools/output/europarl.es-en \
  --alignfn ~/terere/bibletools/output/europarl.es-en.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_default_esen \

cat PROBLEMS
