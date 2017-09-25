#!/bin/bash

cp ~/terere/bibletools/output/bible.es-qu.source.annotated annotated/input.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/input.annotated \
  --clusterfn /space/clustering/brown-spanish-europarl/paths \
  --featureprefix brown_europarl \
  > annotated/output.annotated

mv annotated/output.annotated annotated/input.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/input.annotated \
  --clusterfn /space/clustering/brown-spanish-europarl-lemmas/paths \
  --featureprefix brown_europarl_lemma \
  --lemmas True \
  > annotated/output.annotated

mv annotated/output.annotated annotated/input.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/input.annotated \
  --clusterfn /space/clustering/brown-spanish-wikipedia/paths \
  --featureprefix brown_wikipedia \
  > annotated/output.annotated

mv annotated/output.annotated annotated/input.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/input.annotated \
  --clusterfn /space/clustering/brown-spanish-wikipedia-lemmas/paths \
  --featureprefix brown_wikipedia_lemma \
  --lemmas True \
  > annotated/output.annotated

mv annotated/output.annotated annotated/input.annotated

python3 ./annotate_syntactic.py \
  --annotatedfn annotated/input.annotated \
  --conllfn ~/chipa/src/annotated/bible.es-qu.source.conll.parsed \
  > annotated/output.annotated

rm -f annotated/input.annotated
mv annotated/output.annotated annotated/bible.es-qu.source.annotated
