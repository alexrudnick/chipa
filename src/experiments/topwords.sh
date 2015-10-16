#!/bin/bash

python3 topwords.py \
  --bitextfn ~/terere/bibletools/output/bible.es-gn \
  --alignfn ~/terere/bibletools/output/bible.es-gn.align \
  --annotatedfn ~/terere/bibletools/output/bible.es-gn.source.annotated

python3 topwords.py \
  --bitextfn ~/terere/bibletools/output/bible.es-qu \
  --alignfn ~/terere/bibletools/output/bible.es-qu.align \
  --annotatedfn ~/terere/bibletools/output/bible.es-qu.source.annotated

python3 topwords.py \
  --bitextfn ~/terere/bibletools/output/bible.es-en \
  --alignfn ~/terere/bibletools/output/bible.es-en.align \
  --annotatedfn ~/terere/bibletools/output/bible.es-en.source.annotated

python3 topwords.py \
  --bitextfn ~/terere/bibletools/output/bible.en-es \
  --alignfn ~/terere/bibletools/output/bible.en-es.align \
  --annotatedfn ~/terere/bibletools/output/bible.en-es.source.annotated
