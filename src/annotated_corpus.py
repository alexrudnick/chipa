class Token:
    def __init__(self, lemma, surface):
        self.lemma = lemma
        self.surface = surface
        self.annotations = set()

    def __str__(self):
        annotations = sorted(list(self.annotations))
        out = "{0}\t{1}\t{2}".format(self.lemma,
                                     self.surface,
                                     "\t".join(annotations))
        return out

    def __repr__(self):
        annotations = sorted(list(self.annotations))
        out = "<Token: {0} {1} {2}>".format(self.lemma,
                                              self.surface,
                                              "//".join(annotations))
        return out

    @staticmethod
    def from_string(s):
        lemma, surface, annotations = s.split('\t', maxsplit=2)
        out = Token(lemma, surface)
        out.annotations = set(annotations.split('\t'))
        return out

def load_corpus_from_lines(lines):
    sentences = []
    sentence = []
    for line in lines:
        line = line.strip()
        if line:
            token = Token.from_string(line)
            sentence.append(token)
        elif sentence:
            sentences.append(sentence)
            sentence = []
    if sentence:
        sentences.append(sentence)
    return sentences

def load_corpus(fn):
    """Given a filename, load it up and return a list of list of Tokens. Each
    sublist is a sentence."""
    with open(fn) as infile:
        lines = infile.readlines()
    return load_corpus_from_lines(lines)



def load_corpus_from_lines_for_word(word, lines):
    sentences = []
    sentence = []
    for line in lines:
        line = line.strip()
        if line:
            token = Token.from_string(line)
            sentence.append(token)
        elif sentence:
            if word in [token.lemma for token in sentence]:
                sentences.append(sentence)
            sentence = []
    if sentence:
        if word in [token.lemma for token in sentence]:
            sentences.append(sentence)
    return sentences


def load_corpus_for_word(word, fn):
    """Given a filename, load it up and return a list of list of Tokens. Each
    sublist is a sentence."""
    with open(fn) as infile:
        lines = infile.readlines()
    return load_corpus_from_lines_for_word(word, lines)

def main():
    tok = Token.from_string("cat\tcats\tpos=N\tcategory=animal")
    tok2 = Token.from_string(str(tok))

if __name__ == "__main__": main()
