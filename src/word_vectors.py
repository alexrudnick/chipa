#!/usr/bin/env python3

"""
Code for loading up and returning word vectors.
"""

import numpy as np

class EmbeddingLoader:
    def __init__(self, filename, dimension):
        self.word_to_embedding = {}
        self.dimension = dimension
        self.word_to_embedding = self._load_word_to_embeddings(filename)
        self.mwes = self._pick_mwes()

    def embedding(self, word):
        """Look up embedding for the given word, or if it's not found, return an
        array of 0s in the right width."""
        if word in self.word_to_embedding:
            return self.word_to_embedding[word]
        return np.array([0] * self.dimension)

    def replace_mwes_in_tokens(self, tokens):
        assert type(tokens) is list
        working = " ".join(tokens)
        for mwe in self.mwes:
            joined_mwe = " ".join(mwe)
            if joined_mwe in working:
                replacement = "_".join(mwe)
                working = working.replace(joined_mwe, replacement)
        return working.split()

    def _pick_mwes(self):
        """Builds a list of multiword expressions known by this
        EmbeddingLoader; it's sorted by length in words, then by length in
        characters, longest first."""
        mwes = []
        for key in self.word_to_embedding:
            if "_" in key:
                words = key.split("_")
                if not all(words): continue
                mwes.append(words)
        decorated = [(len(mwe), len("_".join(mwe)), mwe) for mwe in mwes]
        decorated.sort(reverse=True)
        return [mwe for l1,l2,mwe in decorated]

    def _load_word_to_embeddings(self, embeddingfn):
        out = {}
        with open(embeddingfn) as infile:
            _ = infile.readline()
            for line in infile:
                try:
                    word, embeddingstr = line.strip().split(maxsplit=1)
                    embedding = np.array([float(x) 
                                          for x in embeddingstr.split()])
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
            word = loader.replace_mwes_in_tokens([word])[0]
            print(loader.embedding(word))
    except:
        print()

if __name__ == "__main__": main()
