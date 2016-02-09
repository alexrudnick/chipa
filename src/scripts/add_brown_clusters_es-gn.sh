#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/tmp.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/tmp.annotated \
  --clusterfn /space/clustering/brown-spanish-europarl/paths \
  --featureprefix brown_europarl \
  > annotated/tmp2.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/tmp2.annotated \
  --clusterfn /space/clustering/brown-spanish-europarl-lemmas/paths \
  --featureprefix brown_europarl_lemma \
  --lemmas True \
  > annotated/tmp3.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/tmp3.annotated \
  --clusterfn /space/clustering/brown-spanish-wikipedia/paths \
  --featureprefix brown_wikipedia \
  > annotated/bible.es-gn.source.annotated

rm -f annotated/tmp.annotated annotated/tmp2.annotated annotated/tmp3.annotated
