#!/bin/bash

BROWNCLUSTER=$HOME/checkouts/brown-cluster/wcluster

$BROWNCLUSTER \
  --threads 8 \
  --text /space/spanish-wikipedia/spanish-wikipedia-lemmatized.txt \
  --output_dir /space/clustering/brown-spanish-wikipedia-lemmas
