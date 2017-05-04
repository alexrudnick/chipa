#!/bin/bash

WORD2VECDIR=$HOME/checkouts/word2vec/
WORD2VEC=$WORD2VECDIR/word2vec
WORD2PHRASE=$WORD2VECDIR/word2phrase
CORPUS=/space/build_word2vec/europarl-v7.es-en.es.tok

PHRASECORPUS=/space/build_word2vec/europarl-v7.phrase
PHRASECORPUS2=/space/build_word2vec/europarl-v7.phrase2

if [ ! -e "$CORPUS" ]; then
  echo "tokenizing..."
  ~/cdec/corpus/tokenize-anything.sh \
    < /space/europarl-parallel/europarl-v7.es-en.es \
    > $CORPUS
fi

time $WORD2PHRASE -train $CORPUS -output $PHRASECORPUS -threshold 100 -debug 2
time $WORD2PHRASE -train $PHRASECORPUS -output $PHRASECORPUS2 -threshold 100 -debug 2

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-400.cbow \
  -cbow 1 -size 400 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-400.skipgram \
  -cbow 0 -size 400 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-200.cbow \
  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-200.skipgram \
  -cbow 0 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-100.cbow \
  -cbow 1 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-100.skipgram \
  -cbow 0 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-50.cbow \
  -cbow 1 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-europarl-50.skipgram \
  -cbow 0 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 20
