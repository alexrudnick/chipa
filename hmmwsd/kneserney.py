#!/usr/bin/env python3

import nltk
from constants import START

sentences = [
"the dog ran quickly across the yard .",
"i have always relied on the kindness of strangers .",
"what we have here is a failure to communicate .",
"natural language semantics",
]

def trigrams(sentence):
    out = []
    trigram  = (START, START, START)
    for word in sentence.split():
        trigram = trigram[1:] + (word,)
        out.append(trigram)
    return out

model = nltk.model.NgramModel(3, [sentence.split() for sentence in sentences])

fd = nltk.probability.FreqDist()
for sentence in sentences:
    events = trigrams(sentence)
    for event in events:
        fd.inc(event)

kn = nltk.probability.KneserNeyProbDist(fd)
for sentence in sentences:
    events = trigrams(sentence)
    for event in events:
        print("[kn]")
        print(event, kn.prob(event))
        newvent = event[:2] + ("food",)
        print(newvent, kn.prob(newvent))
        print("[default ngrammodel]")
        lastword = event[-1]
        context = event[:2]
        print(event, model.prob(lastword, context=context))
        lastword = "food"
        print(context, lastword, model.prob(lastword, context=context))
