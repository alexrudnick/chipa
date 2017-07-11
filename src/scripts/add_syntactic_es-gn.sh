#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/tmp.annotated

python3 ./annotate_syntactic.py \
  --annotatedfn annotated/tmp.annotated \
  --conllfn ~/chipa/src/annotated/bible.es-gn.source.conll.parsed \
  > annotated/bible.es-gn.source.annotated

rm -f annotated/tmp.annotated
