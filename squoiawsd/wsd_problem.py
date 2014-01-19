#!/usr/bin/env python3

import nltk

START = "QQQSTARTHEADQQQ"
END = "QQQENDHEADQQQ"

class WSDProblem:
    """Class where we'll stash all the information about a given WSD problem."""

    def __init__(self, source_lex, context,
                 testset=False, instance_id=None, head_index=None):
        """Given the source lexical item (ie, uninflected version of the source
        word) and the context, build a WSD problem that we can solve later."""
        self.source_lex = source_lex
        self.instance_id = instance_id
        self.init_testset(context)

    def init_testset(self, context):
        """If we're coming from the test set, we haven't tagged yet. Probably
        tag now. Also we're probably not tokenized."""
        assert type(context) is str
        self.head_indices = []

        context = context.replace("<head>", " " + START)
        ## XXX(alexr): this is completely terrible.
        context = context.replace("</head>", END + " ")

        sentences = nltk.sent_tokenize(context)
        tokenized = [nltk.word_tokenize(sent) for sent in sentences]

        index = 0
        for sent_index,sent in enumerate(tokenized):
            for word_index,word in enumerate(sent):
                if word.startswith(START):
                    if not word.endswith(END):
                        print(repr(word))
                        print(tokenized)
                        print(context)
                        assert False
                    sent[word_index] = word.replace(START,"").replace(END,"")
                    self.head_indices.append(index)
                index += 1
        self.tokenized = []
        for sent in tokenized:
            self.tokenized += sent

    def __str__(self):
        return "<<{0}: {1}>>".format(self.source_lex, self.tagged)
