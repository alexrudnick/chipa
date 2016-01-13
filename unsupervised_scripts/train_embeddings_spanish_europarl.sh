#!/bin/bash

WORD2VECDIR=/home/alex/checkouts/word2vec/
WORD2VEC=$WORD2VECDIR/word2vec
DISTANCE=$WORD2VECDIR/distance
CORPUS=/tmp/europarl-v7.es-en.es.tok

if [ ! -e "/tmp/europarl-v7.es-en.es.tok" ]; then
  echo "tokenizing..."
  ~/cdec/corpus/tokenize-anything.sh \
    < /space/europarl-parallel/europarl-v7.es-en.es \
    > /tmp/europarl-v7.es-en.es.tok
fi

time $WORD2VEC -train $CORPUS \
  -output /space/clustering/word2vec-spanish-europarl-200 \
  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $CORPUS \
  -output /space/clustering/word2vec-spanish-europarl-100 \
  -cbow 1 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $CORPUS \
  -output /space/clustering/word2vec-spanish-europarl-50 \
  -cbow 1 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15
