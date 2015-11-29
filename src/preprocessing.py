#!/usr/bin/env python3

## TODO(alexr): We need to get these run through the whole preprocessing
## pipeline so we can evaluate the semeval test set. 

## We need to be able to call freeling programmatically.
## And probably also cdec's tokenizer.

## XXX: magic string pointing into my files on my one particular computer.
FREELINGCONFIGDIR = "/home/alex/terere/bibletools/freeling-config"

import fileinput
from subprocess import Popen, PIPE, STDOUT

import nltk

from annotated_corpus import Token

def tokenize(sentence, sl):
    """Tokenize input sentence, given as a string."""
    assert isinstance(sentence, str)
    return nltk.word_tokenize(sentence)

def annotate(sentence, sl):
    """Given an input sentence as a tokenized list of strings, return a list of
    Token objects."""
    assert isinstance(sentence, list)
    out = []
    for word in sentence:
        token = Token(word.lower(), word)
        out.append(token)
    return out

## XXX: this assumes that Freeling is installed on the system and that we have a
## path to a directory of config files.
def run_freeling(sentence, sl):
    assert isinstance(sentence, str)
    with Popen(["analyze", "-f", FREELINGCONFIGDIR + "/" + sl + ".cfg"],
              stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
        stdout_b = p.communicate(input=sentence.encode("utf-8"))
        print(stdout_b[0].decode("utf-8"))

def preprocess(sentence, sl):
    """Run the preprocessing pipeline on the sentence, which should be a
    string."""
    assert isinstance(sentence, str)
    run_freeling(sentence, sl)

    words = tokenize(sentence, sl)
    return annotate(words, sl)

def main():
    for line in fileinput.input():
        line = line.strip()
        preprocessed = preprocess(line, "es")
        print(preprocessed)

if __name__ == "__main__": main()
