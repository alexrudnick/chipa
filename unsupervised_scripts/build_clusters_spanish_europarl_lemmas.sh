#!/bin/bash

BROWNCLUSTER=$HOME/checkouts/brown-cluster/wcluster

$BROWNCLUSTER \
  --threads 8 \
  --text $HOME/terere/bibletools/output/europarl.en-es.target.lemmas \
  --output_dir /space/clustering/brown-spanish-europarl-lemmas
