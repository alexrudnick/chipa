#!/bin/bash

python3 learn.py \
  --targetlang=es \
  --sourcetext=/space/Europarl_Intersection_preprocessed/intersection.en.txt.ascii \
  --targettext=/space/Europarl_Intersection_preprocessed/intersection.es.txt \
  --alignments=/space/output_en_es/training.align \

  ## --fast=False \

