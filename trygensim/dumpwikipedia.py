#!/usr/bin/env python3

"""Script to dump an entire Wikipedia archive and split it into sentences.
"""

import sys

import nltk
import gensim
from gensim.corpora import WikiCorpus

import os.path
import sys

## We're going to replace gensim.corpora.wikicorpus.tokenize with this, so that
## we get NLTK sentence splitting and don't drop punctuation.
def replacement_tokenize(content):
    return [token.encode('utf-8') for token in nltk.word_tokenize(content)]

def main():
    gensim.corpora.wikicorpus.tokenize = replacement_tokenize

    infn, outfn = sys.argv[1:3]
    wiki = WikiCorpus(infn, lemmatize=False, dictionary={})
    with open(outfn, 'w') as outfile:
        for i, article in enumerate(wiki.get_texts()):
            article = [entry.decode("utf-8") for entry in article]
            text = " ".join(article)
            sentences = nltk.sent_tokenize(text)
            for sentence in sentences:
                print(sentence, file=outfile)
            if (i % 10000 == 0):
                print("Saved ", i, "articles")
 
if __name__ == '__main__': main()

