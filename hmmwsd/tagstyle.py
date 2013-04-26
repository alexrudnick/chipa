def get_tagger_and_cfd(args):
    triple_sentences = load_bitext(args)
    print("training on {0} sentences.".format(len(triple_sentences)))
    tagger, cfd = build_tagger_and_cfd(triple_sentences)
    return tagger, cfd

def build_tagger_and_cfd(triple_sentences):
    """Builds the tagger and a conditional freqdist."""

    cfd = nltk.probability.ConditionalFreqDist()
    sentences = []
    for (ss, ts, alignment) in triple_sentences:
        tws = target_words_for_each_source_word(ss, ts, alignment)
        tagged = list(zip(ss, tws))
        ## XXX(alexr): this is sort of ridiculous
        nozeros = [(source, target) for (source,target) in tagged if target]

        for (source, target) in nozeros:
            cfd[source].inc(target)
        # print(nozeros)
        sentences.append(nozeros)

    tagger = nltk.tag.HiddenMarkovModelTagger.train(sentences)
    return tagger, cfd

