#!/usr/bin/env python3

"""
Go through an annotated corpus and remove specified annotations. Print the
result to stdout.
"""
import argparse

import annotated_corpus

def get_argparser():
    parser = argparse.ArgumentParser(description='annotate_brown')
    parser.add_argument('--annotatedfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    corpus = annotated_corpus.load_corpus(args.annotatedfn)

    for sentence in corpus:
        for token in sentence:
            for annotation in list(token.annotations):
                # XXX: change what you need to remove here
                if annotation.startswith("stack_bible_"):
                    token.annotations.remove(annotation)
                if annotation.startswith("child_lemma"):
                    token.annotations.remove(annotation)
                if annotation.startswith("head_lemma"):
                    token.annotations.remove(annotation)
                if annotation.startswith("head_surface"):
                    token.annotations.remove(annotation)
                if annotation.startswith("child_surface"):
                    token.annotations.remove(annotation)
            print(token)
        print()

if __name__ == "__main__": main()
