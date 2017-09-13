#!/bin/bash

cp ~/terere/bibletools/output/bible.es-qu.source.annotated annotated/tmp.annotated

python3 ./annotate_syntactic.py \
  --annotatedfn annotated/tmp.annotated \
  --conllfn ~/chipa/src/annotated/bible.es-qu.source.conll.parsed \
  > annotated/bible.es-qu.source.annotated

rm -f annotated/tmp.annotated
