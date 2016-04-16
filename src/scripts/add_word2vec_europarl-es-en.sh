#!/bin/bash

cp ~/terere/bibletools/output/bible.es-en.source.annotated annotated/tmp.annotated

python3 annotate_word2vec.py \
  --annotatedfn annotated/tmp.annotated \
  --embeddingfn /space/clustering/word2vec-spanish-europarl-100 \
  --featureprefix word2vec_europarl \
  > annotated/bible.es-en.source.annotated

rm -f annotated/tmp.annotated annotated/tmp2.annotated
