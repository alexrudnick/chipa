#!/bin/bash

cp ~/terere/bibletools/output/bible.es-qu.source.annotated annotated/tmp.annotated

python3 annotate_doc2vec.py \
  --annotatedfn annotated/tmp.annotated \
  --doc2vecmodel /space/chipa/trygensim/200-spanish-wikipedia-doc2vec.model \
  --featureprefix doc2vec_wikipedia \
  > annotated/bible.es-qu.source.annotated

rm -f annotated/tmp.annotated
