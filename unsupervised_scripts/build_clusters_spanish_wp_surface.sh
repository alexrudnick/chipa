#!/bin/bash

BROWNCLUSTER=/home/alex/checkouts/brown-cluster/wcluster

$BROWNCLUSTER \
  --threads 8 \
  --text /space/spanish-wikipedia/spanish-wikipedia.txt \
  --output_dir /space/clustering/brown-spanish-wikipedia