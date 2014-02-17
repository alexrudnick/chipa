import sys

def print_lemmatized_sentences(sentences):
    for sent in sentences:
        line = " ".join(lemma for (token,lemma) in sent)
        if line.lower().startswith("-- warning"): continue
        print(line)

def print_tokenized_sentences(sentences):
    for sent in sentences:
        line = " ".join(token for (token,lemma) in sent)
        if line.lower().startswith("-- warning"): continue
        line = line.replace("_", " ")
        print(line)

def dprint(*a,**aa):
    print(file=sys.stderr, *a, **aa)
