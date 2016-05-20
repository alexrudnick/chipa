#!/usr/bin/env python3

"""Script to dump an entire Wikipedia archive and split it into sentences.
"""

import sys
import nltk
from gensim.corpora import WikiCorpus

import os.path
import sys

def main():
    infn, outfn = sys.argv[1:3]
    i = 0

    ## XXX: this seems to be dropping punctuation currently, so we're not
    ## getting sentence splitting.
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

