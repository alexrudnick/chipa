#!/bin/bash

cp ~/terere/bibletools/output/bible.es-gn.source.annotated annotated/tmp.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/tmp.annotated \
  --clusterfn /space/build_brown_clusters/europarl-v7.es-gn.es-c512-p1.out/paths \
  --featureprefix brown_europarl \
  > annotated/tmp2.annotated

python3 annotate_brown.py \
  --annotatedfn annotated/tmp2.annotated \
  --clusterfn /space/build_brown_clusters/bible.es-c512-p1.out/paths \
  --featureprefix brown_bible \
  > annotated/bible.es-gn.source.annotated

rm -f annotated/tmp.annotated annotated/tmp2.annotated
