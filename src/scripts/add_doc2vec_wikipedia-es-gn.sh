#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/tmp.annotated

python3 annotate_doc2vec.py \
  --annotatedfn annotated/tmp.annotated \
  --doc2vecmodel /space/chipa/trygensim/spanish-wikipedia-doc2vec.model \
  --featureprefix doc2vec_wikipedia \
  > annotated/bible.es-gn.source.annotated

rm -f annotated/tmp.annotated
