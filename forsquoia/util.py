import sys

def print_lemmatized_sentences(sentences):
    for sent in sentences:
        line = " ".join(lemma for (token,lemma) in sent)
        if line.startswith("-- warning"): continue
        print(line)

def dprint(*a,**aa):
    print(file=sys.stderr, *a, **aa)