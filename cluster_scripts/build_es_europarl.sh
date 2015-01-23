#!/bin/bash

~/cdec/corpus/tokenize-anything.sh \
  < /space/europarl-bitext-nonintersected/europarl-v7.es-en.es \
  | ~/cdec/corpus/lowercase.pl \
  > europarl-v7.es-en.es.tok

~/checkouts/brown-cluster/wcluster \
  --text ./europarl-v7.es-en.es.tok \
  --c 512 \
  --threads 4 \
