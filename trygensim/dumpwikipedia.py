#!/usr/bin/env python3

"""Script to dump an entire Wikipedia archive and split it into sentences.

Takes a wikipedia archive like eswiki-latest-pages-articles.xml.bz2 and an
output file as arguments.

python3 dumpwikipedia.py eswiki-latest-pages-articles.xml.bz2 eswiki.txt
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
    ## Just split on spaces; we're going to use freeling to tokenize later.
    return [token.encode('utf-8') for token in content.split(' ')]

def cleanup(sentence):
    ## remove == or === marking headings
    if sentence.startswith("==="):
        sentence = sentence[3:]
        if sentence.endswith("==="):
            sentence = sentence[:-3]
    elif sentence.startswith("=="):
        sentence = sentence[2:]
        if sentence.endswith("=="):
            sentence = sentence[:-2]
    elif sentence.startswith("**"):
        sentence = sentence[2:]
    elif sentence.startswith("*"):
        sentence = sentence[1:]
    return sentence.strip()


def main():
    gensim.corpora.wikicorpus.tokenize = replacement_tokenize

    infn, outfn = sys.argv[1:3]
    wiki = WikiCorpus(infn, lemmatize=False, dictionary={})
    with open(outfn, 'w') as outfile:
        for i, article in enumerate(wiki.get_texts()):
            article = [entry.decode("utf-8") for entry in article]
            text = " ".join(article)
            mostly_sentences = nltk.sent_tokenize(text)

            sentences = []
            for sent in mostly_sentences:
                for line in sent.splitlines():
                    sentences.append(line.strip())

            for sentence in sentences:
                sentence = cleanup(sentence)
                if sentence:
                    print(sentence, file=outfile)
            if (i % 10000 == 0):
                print("Saved ", i, "articles")
 
if __name__ == '__main__': main()

