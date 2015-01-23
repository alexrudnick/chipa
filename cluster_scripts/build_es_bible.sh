#!/bin/bash

cut -f 2 ~/terere/bibletools/output/bible.es \
  | ~/cdec/corpus/tokenize-anything.sh \
  | ~/cdec/corpus/lowercase.pl \
  > ./bible.es.tok

~/checkouts/brown-cluster/wcluster \
  --text ./bible.es.tok \
  --c 512 \
  --threads 4 \
