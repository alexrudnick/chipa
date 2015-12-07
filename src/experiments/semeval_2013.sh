#!/bin/bash

python3 semeval_experiment.py \
  --bitext ~/terere/bibletools/output/europarl.en-es \
  --alignfn ~/terere/bibletools/output/europarl.en-es.align \
  --annotatedfn annotated/europarl.en-es.source.annotated \
  --featurefn $@ \
  --testset /home/alex/checkouts/semeval2013/finaltest/
