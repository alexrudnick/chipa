#!/bin/bash

python3 ./annotate_clwsd.py \
  --annotatedfn ~/terere/bibletools/output/europarl.es-de.source.annotated \
  --bitext ~/terere/bibletools/output/europarl.es-de \
  --alignfn ~/terere/bibletools/output/europarl.es-de.align \
  --featurefn featuresets/default.features \
  --annotated_to_classify annotated/bible.es-gn.source.annotated \
  --featureprefix stack_default_esde \

cat PROBLEMS
