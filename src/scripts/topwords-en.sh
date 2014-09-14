#!/bin/bash

python3 topwords.py \
  --bitext ~/terere/bibletools/bible.es-en \
  --alignfn ~/terere/bibletools/bible.es-en.align \
  --surfacefn ~/terere/bibletools/bible.es-en.surface
mv topwords-translations.txt topwords-translations.es-en
mv topwords.txt topwords-es.txt

python3 topwords.py \
  --bitext ~/terere/bibletools/bible.en-es \
  --alignfn ~/terere/bibletools/bible.en-es.align \
  --surfacefn ~/terere/bibletools/bible.en-es.surface
mv topwords-translations.txt topwords-translations.en-es
mv topwords.txt topwords-en.txt
