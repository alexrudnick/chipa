#!/usr/bin/env python3

import argparse

from pymongo import MongoClient

"""Take a pre-tokenized bitext corpus in source ||| target (one sentence per
line) format and save it in the db."""


def init_collection(db, collection):
    collection = db[collection]
    collection.drop()

def sentence_generator(fn):
    ## TODO: store alignments too
    with open(fn) as infile:
        for line in infile:
            line = line.strip()
            assert line.count("|||") == 1
            source, target = line.split("|||")
            source = source.strip()
            target = target.strip()
            yield {"source":source,
                   "target":target}

def store_sentences(fn, db, collection):
    sentences = sentence_generator(fn)
    db[collection].insert(sentences)

def init_index(db, collection):
    ## index on the "source" field, make sure it's a text index
    db[collection].ensure_index(
        [('source', 'text'),
         ('target', 'text')])

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='import_bitext')
    parser.add_argument('--bitext', type=str, required=True)
    parser.add_argument('--collection', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    bitextfn = args.bitext
    collection = args.collection

    client = MongoClient()
    db = client['corpus']

    init_collection(db, collection)
    store_sentences(bitextfn, db, collection)
    init_index(db, collection)
    print("OK.")

if __name__ == "__main__": main()
