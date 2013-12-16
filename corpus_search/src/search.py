#!/usr/bin/env python3

import argparse

from pymongo import MongoClient

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='search')
    parser.add_argument('--collection', type=str, required=True)
    return parser

res = None

def main():
    global res
    parser = get_argparser()
    args = parser.parse_args()
    collection = args.collection

    client = MongoClient()
    db = client['corpus']

    while True:
        try:
            q = input("> ")
            q = q.strip()
            if not q: continue
            ## TODO: this seems to only pull 100 at max
            res = db.command('text', collection, search=q)
            results = res['results']
            print("GOT THIS MANY RESULTS:", len(results))
            for r in results:
                print("source:", r['obj']['source'])
                print("target:", r['obj']['target'])
        except:
            print()
            break
    print("OK.")

if __name__ == "__main__": main()



