#!/bin/bash

# cp ~/terere/bibletools/output/bible.es-gn.source.annotated
#    annotated/tmp.annotated
cp annotated/bible.es-gn.source.annotated annotated/tmp.annotated

python3 annotated2conllx.py --annotatedfn annotated/tmp.annotated \
  > ~/chipa/src/annotated/bible.es-gn.source.conll

pushd ~/chipa/maltparser/espmalt
java -Xmx4096m -jar ~/chipa/maltparser/maltparser-1.9.0/maltparser-1.9.0.jar \
  -c espmalt-1.0 -i ~/chipa/src/annotated/bible.es-gn.source.conll \
  -o ~/chipa/src/annotated/bible.es-gn.source.conll.parsed -m parse
popd

python3 ./annotate_syntactic.py \
  --annotatedfn annotated/tmp.annotated \
  --conllfn ~/chipa/src/annotated/bible.es-gn.source.conll.parsed \
  > annotated/bible.es-gn.source.annotated

rm annotated/tmp.annotated
