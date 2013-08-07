#!/bin/bash

echo "unigrams"
cat HMMoutput_unigram/*results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "bigrams"
cat HMMoutput_bigram/*results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "trigrams"
cat HMMoutput_trigram/*results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "memms"
cat MEMMoutput_trigram/*results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py

echo "maxent"
cat MEMMoutput_maxent/*results | grep "^precision =" | cut -f 3 -d " " | sed "s/,//g"  | sum_numbers.py
