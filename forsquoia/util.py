def print_lemmatized_sentences(sentences):
    for sent in sentences:
        print(" ".join(lemma for (token,lemma) in sent))

