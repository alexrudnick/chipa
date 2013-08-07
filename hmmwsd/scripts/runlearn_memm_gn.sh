#!/bin/bash

python3 learn_memm.py \
  --targetlang=gn \
  --sourcetext=/space/es_gn_bibles/bible.es.txt \
  --targettext=/space/es_gn_bibles/bible.gn.txt \
  --alignments=/space/output_es_gn/training.align \
  ## --fast=True \

