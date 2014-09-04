import features

from constants import UNTRANSLATED

SL_SENTENCES = None
TAGGED_SENTENCES = None
SL_SENTENCES_SURFACE = None

def set_examples(sl_sentences, tagged_sentences):
    global SL_SENTENCES
    global TAGGED_SENTENCES
    SL_SENTENCES = sl_sentences
    TAGGED_SENTENCES = tagged_sentences

def set_sl_surface_sentences(surface_sentences):
    global SL_SENTENCES_SURFACE
    global SL_SENTENCES
    SL_SENTENCES_SURFACE = surface_sentences

    assert len(SL_SENTENCES_SURFACE) == len(SL_SENTENCES)

def build_instance(tagged_sentence, surface, index):
    feat = features.extract(tagged_sentence, surface, index)
    label = tagged_sentence[index][1]
    return (feat, label)

def trainingdata_for(word, nonnull=False):
    training = []
    for (sent_index, (ss,tagged)) in enumerate(zip(SL_SENTENCES, TAGGED_SENTENCES)):
        ## XXX: what if the word is in the source sentence more than once?
        if word in ss:
            index = ss.index(word)
            surface = SL_SENTENCES_SURFACE[sent_index]
            training.append(build_instance(tagged, surface, index))
    if nonnull:
        training = [(feat,label) for (feat,label) in training
                                 if label != UNTRANSLATED]

    return training
    ## XXX: just take the first 50 instances
    ## return training[:50]

def load_bitext_twofiles(bitextfn, alignfn):
    """Take in bitext filename and then alignment filename.
    Return a list of (source,target,alignment) tuples. Lowercase everything.
    NB: input files should already be tokenized and lemmatized at this point.
    """
    out_source = []
    out_target = []
    out_align = []

    with open(bitextfn) as infile_bitext, \
         open(alignfn) as infile_align:
        for bitext, alignment in zip(infile_bitext, infile_align):
            source, target = bitext.split("|||")
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
    return list(zip(out_source, out_target, out_align))

def load_surface_file(surfacebitextfn):
    """Load up the 'surface' version of the bitext. We're just going to store
    the source side for now."""
    out_source = []
    with open(surfacebitextfn) as infile_bitext:
        for bitext in infile_bitext:
            source, target = bitext.split("|||")
            out_source.append(source.strip().lower().split())
    return out_source
