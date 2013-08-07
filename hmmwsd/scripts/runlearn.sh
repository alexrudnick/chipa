#!/bin/bash

python3 learn.py \
  --targetlang=es \
  --sourcetext=/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii.taggedlemmas \
  --targettext=/space/Europarl_Intersection_preprocessed/intersection.es.txt.lemmas \
  --alignments=/space/output_en_es/training.align \
  # --fast=True \

