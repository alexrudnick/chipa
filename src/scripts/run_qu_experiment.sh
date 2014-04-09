#!/bin/bash

python3 qu_experiment.py \
  --sourcefn /space/output_es_qu/training.es.txt \
  --targetfn /space/output_es_qu/training.qu.txt \
  --alignfn /space/output_es_qu/training.align \
  --crossvalidate \
  "$@" \
