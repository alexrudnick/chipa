#!/usr/bin/env python3

"""
Code for loading up and returning word vectors.
"""

import numpy as np

class EmbeddingLoader:
    def __init__(self, filename, dimension):
        self.word_to_embedding = {}
        self.dimension = dimension
        self.word_to_embedding = self.load_word_to_embeddings(filename)

    def embedding(self, word):
        """Look up embedding for the given word, or if it's not found, return an
        array of 0s in the right width."""
        if word in self.word_to_embedding:
            return self.word_to_embedding[word]
        return np.array([0] * self.dimension)

    def load_word_to_embeddings(self, embeddingfn):
        out = {}
        with open(embeddingfn) as infile:
            _ = infile.readline()
            for line in infile:
                try:
                    word, embeddingstr = line.strip().split(maxsplit=1)
                    embedding = [float(x) for x in embeddingstr.split()]
                    out[word] = embedding
                except UnicodeDecodeError as e:
                    continue
        return out

def main():
    """quick demo main for looking up embeddings"""
    import sys
    import readline
    filename = sys.argv[1]
    dimension = int(sys.argv[2])
    loader = EmbeddingLoader(filename, dimension)
    print("loaded.")
    try:
        while True:
            word = input("word: ")
            print(loader.embedding(word))
    except:
        print()

if __name__ == "__main__": main()
