#!/bin/bash

WORD2VECDIR=$HOME/checkouts/word2vec/
WORD2VEC=$WORD2VECDIR/word2vec
WORD2PHRASE=$WORD2VECDIR/word2phrase
CORPUS=/space/spanish-wikipedia/spanish-wikipedia.txt

PHRASECORPUS=/space/spanish-wikipedia/spanish-wikipedia-phrase.txt
PHRASECORPUS2=/space/spanish-wikipedia/spanish-wikipedia-phrase2.txt

time $WORD2PHRASE -train $CORPUS -output $PHRASECORPUS -threshold 100 -debug 2
time $WORD2PHRASE -train $PHRASECORPUS -output $PHRASECORPUS2 -threshold 100 -debug 2

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-400.cbow \
  -cbow 1 -size 400 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-400.skipgram \
  -cbow 0 -size 400 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-200.cbow \
  -cbow 1 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-200.skipgram \
  -cbow 0 -size 200 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-100.cbow \
  -cbow 1 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-100.skipgram \
  -cbow 0 -size 100 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-50.cbow \
  -cbow 1 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100

time $WORD2VEC -train $PHRASECORPUS2 \
  -output /space/clustering/word2vec-spanish-wikipedia-50.skipgram \
  -cbow 0 -size 50 -window 8 -negative 25 -hs 0 -sample 1e-4 \
  -threads 20 -binary 0 -iter 15 -min-count 100
