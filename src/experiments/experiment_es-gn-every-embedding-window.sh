#!/bin/bash

set -eu
set -o pipefail

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-europarl-50.cbow \
  --embedding_dim 50 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-europarl-100.cbow \
  --embedding_dim 100 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-europarl-200.cbow \
  --embedding_dim 200 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-europarl-400.cbow \
  --embedding_dim 400 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-wikipedia-50.cbow \
  --embedding_dim 50 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-wikipedia-100.cbow \
  --embedding_dim 100 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-wikipedia-200.cbow \
  --embedding_dim 200 \
  --window True

python3 clwsd_experiment_embeddings.py \
  --bitext ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/chipa/src/annotated/bible.es-gn.source.annotated \
  --embeddings /space/clustering/word2vec-spanish-wikipedia-400.cbow \
  --embedding_dim 400 \
  --window True
