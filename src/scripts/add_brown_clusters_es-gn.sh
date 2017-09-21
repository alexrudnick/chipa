#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/input.annotated

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
  > annotated/bible.es-gn.source.annotated

rm -f annotated/input.annotated
rm -f annotated/output.annotated
