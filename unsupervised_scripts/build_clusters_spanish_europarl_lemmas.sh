#!/bin/bash

BROWNCLUSTER=/home/alex/checkouts/brown-cluster/wcluster

$BROWNCLUSTER \
  --threads 8 \
  --text /home/alex/terere/bibletools/output/europarl.en-es.target.lemmas \
  --output_dir /space/clustering/brown-spanish-europarl-lemmas
