#!/bin/bash

## XXX: we need to preprocess europarl; using the Bible is not going to help us
## here.
python3 semeval_experiment.py \
  --bitext ~/terere/bibletools/output/bible.en-es \
  --alignfn ~/terere/bibletools/output/bible.en-es.align \
  --annotatedfn annotated/bible.en-es.source.annotated \
  --featurefn $@ \
  --testset /home/alex/checkouts/semeval2013/finaltest/range.data
