#!/bin/bash

WORD2VECDIR=/home/alex/checkouts/word2vec/
WORD2VEC=$WORD2VECDIR/word2vec
WORD2PHRASE=$WORD2VECDIR/word2phrase
CORPUS=/tmp/europarl-v7.es-en.es.tok

PHRASECORPUS=/tmp/europarl-v7.phrase
PHRASECORPUS2=/tmp/europarl-v7.phrase2

if [ ! -e "/tmp/europarl-v7.es-en.es.tok" ]; then
  echo "tokenizing..."
  ~/cdec/corpus/tokenize-anything.sh \
    < /space/europarl-parallel/europarl-v7.es-en.es \
    > /tmp/europarl-v7.es-en.es.tok
fi

time $WORD2PHRASE -train $CORPUS -output $PHRASECORPUS -threshold 100 -debug 2
time $WORD2PHRASE -train $PHASECORPUS -output $PHRASECORPUS2 -threshold 100 -debug 2

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-200.cbow \
  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-200.skipgram \
  -cbow 0 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-100.cbow \
  -cbow 1 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-100.skipgram \
  -cbow 0 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-50.cbow \
  -cbow 1 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-50.skipgram \
  -cbow 0 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15
