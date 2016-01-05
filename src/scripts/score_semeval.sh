#!/bin/bash 

THELANGS="es"
WORDS="coach education execution figure job letter match mission mood paper post pot range rest ring scene side soil strain test"

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semeval_2013_output/"$WORD"."$THELANG".oof ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt -t oof
    perl scripts/ScorerTask3.pl ../semeval_2013_output/"$WORD"."$THELANG".oof ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt -t oof
  done
done

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semeval_2013_output/"$WORD"."$THELANG".best ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt
    perl scripts/ScorerTask3.pl ../semeval_2013_output/"$WORD"."$THELANG".best ../semeval_2013_gold/"$THELANG"/"$WORD"_gold.txt
  done
done


for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semeval_2010_output/"$WORD"."$THELANG".oof ../semeval_2010_gold/"$WORD".gold."$THELANG" -t oof
    perl scripts/ScorerTask3.pl ../semeval_2010_output/"$WORD"."$THELANG".oof ../semeval_2010_gold/"$WORD".gold."$THELANG" -t oof
  done
done

for THELANG in $THELANGS; do
  for WORD in $WORDS; do
    echo perl scripts/ScorerTask3.pl ../semeval_2010_output/"$WORD"."$THELANG".best ../semeval_2010_gold/"$WORD".gold."$THELANG"
    perl scripts/ScorerTask3.pl ../semeval_2010_output/"$WORD"."$THELANG".best ../semeval_2010_gold/"$WORD".gold."$THELANG"
  done
done

echo "==== 2013 precision best ===="
cat ../semeval_2013_output/*.best.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "==== 2013 precision oof ===="
cat ../semeval_2013_output/*.oof.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py


echo "==== 2010 precision best ===="
cat ../semeval_2010_output/*.best.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "==== 2010 precision oof ===="
cat ../semeval_2010_output/*.oof.results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py
