#!/usr/bin/env python3

import fileinput

sentence = []
for line in fileinput.input():
    word = line.strip()
    if not word:
        print(" ".join(sentence))
        sentence = []
    else:
        sentence.append(word)
