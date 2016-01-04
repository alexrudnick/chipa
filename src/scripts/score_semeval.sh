#!/bin/bash 

THELANGS="es"
WORDS="coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test"

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semevaloutput/"$WORD"."$THELANG".oof ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt -t oof
    perl scripts/ScorerTask3.pl ../semevaloutput/"$WORD"."$THELANG".oof ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt -t oof
  done
done

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semevaloutput/"$WORD"."$THELANG".best ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt
    perl scripts/ScorerTask3.pl ../semevaloutput/"$WORD"."$THELANG".best ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt
  done
done

echo "==== 2013 precision best ===="
cat ../semevaloutput/*.best.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "==== 2013 precision oof ===="
cat ../semevaloutput/*.oof.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py
