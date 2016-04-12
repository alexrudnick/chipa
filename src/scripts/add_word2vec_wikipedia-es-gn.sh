#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/tmp.annotated

python3 annotate_word2vec.py \
  --annotatedfn annotated/tmp.annotated \
  --embeddingfn /space/clustering/word2vec-spanish-wikipedia-100 \
  --featureprefix word2vec_wikipedia \
  > annotated/bible.es-gn.source.annotated

rm -f annotated/tmp.annotated
