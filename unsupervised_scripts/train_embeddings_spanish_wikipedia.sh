#!/bin/bash

WORD2VECDIR=/home/alex/checkouts/word2vec/
WORD2VEC=$WORD2VECDIR/word2vec
DISTANCE=$WORD2VECDIR/distance

CORPUS=/space/spanish-wikipedia/spanish-wikipedia.txt

time $WORD2VEC -train $CORPUS \
  -output /clustering/word2vec-spanish-wikipedia-200 \
  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $CORPUS \
  -output /clustering/word2vec-spanish-wikipedia-100 \
  -cbow 1 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $CORPUS \
  -output /clustering/word2vec-spanish-wikipedia-50 \
  -cbow 1 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15
