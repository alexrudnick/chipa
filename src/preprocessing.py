#!/usr/bin/env python3

## TODO(alexr): We need to get these run through the whole preprocessing
## pipeline so we can evaluate the semeval test set. 

## We need to be able to call freeling programmatically.
## And probably also cdec's tokenizer.

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

def preprocess(sentence, sl):
    """Run the preprocessing pipeline on the sentence, which should be a
    string."""
    assert isinstance(sentence, str)
    words = tokenize(sentence, sl)
    return annotate(words, sl)
