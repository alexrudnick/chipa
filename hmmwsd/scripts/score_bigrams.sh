#!/bin/bash 

# THELANGS="de es fr it nl"
THELANGS="es"
WORDS="coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test"

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl HMMoutput_bigram/"$WORD"."$THELANG".best gold/"$THELANG"/"$WORD"_gold.txt -t best
    perl scripts/ScorerTask3.pl HMMoutput_bigram/"$WORD"."$THELANG".best gold/"$THELANG"/"$WORD"_gold.txt -t best
  done
done
