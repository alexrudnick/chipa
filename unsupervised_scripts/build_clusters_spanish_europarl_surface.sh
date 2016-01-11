#!/bin/bash

BROWNCLUSTER=/home/alex/checkouts/brown-cluster/wcluster

~/cdec/corpus/tokenize-anything.sh \
  < /space/europarl-parallel/europarl-v7.es-en.es \
  > /tmp/europarl-v7.es-en.es.tok

$BROWNCLUSTER \
  --threads 8 \
  --text /tmp/europarl-v7.es-en.es.tok \
  --output_dir /space/clustering/brown-spanish-europarl
