from operator import itemgetter
import functools
import re

import nltk

import features
import util
from constants import UNTRANSLATED

SL_SENTENCES = None
TAGGED_SENTENCES = None
SL_SENTENCES_ANNOTATED = None

STOPWORDS = []

def set_examples(sl_sentences, tagged_sentences):
    global SL_SENTENCES
    global TAGGED_SENTENCES
    SL_SENTENCES = sl_sentences
    TAGGED_SENTENCES = tagged_sentences

def set_sl_annotated(sl_annotated):
    global SL_SENTENCES_ANNOTATED
    global SL_SENTENCES

    SL_SENTENCES_ANNOTATED = sl_annotated
    surface_sentences = []
    for sentence in sl_annotated:
        surface_sent = [token.surface for token in sentence]
        surface_sentences.append(surface_sent)
    assert len(SL_SENTENCES_ANNOTATED) == len(SL_SENTENCES), \
        "{0} vs {1}".format(len(SL_SENTENCES_ANNOTATED), len(SL_SENTENCES))

def build_instance(tagged_sentence, annotated, index):
    feat = features.extract(tagged_sentence, annotated, index)
    label = tagged_sentence[index][1]
    return (feat, label)

@functools.lru_cache(maxsize=100000)
def trainingdata_for(word, nonnull=False):
    assert type(word) is str
    training = []
    for (sent_index, (ss,tagged)) in enumerate(zip(SL_SENTENCES, TAGGED_SENTENCES)):
        ## XXX: what if the word is in the source sentence more than once?
        if word in ss:
            index = ss.index(word)
            annotated = SL_SENTENCES_ANNOTATED[sent_index]
            training.append(build_instance(tagged, annotated, index))
    if nonnull:
        training = [(feat,label) for (feat,label) in training
                                 if label != UNTRANSLATED]
    ## XXX: just take the first 50 instances
    ## return training[:50]
    return training

## XXX: what we should be doing here is setting the corpus so that we know what
## words we're going to be looking for ahead of time.
## as we go through, save the training data for each relevant word.

def load_bitext(bitextfn, alignfn):
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

def load_bitext_for_word(word, bitextfn, alignfn):
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
            if word not in (source.strip().lower().split()):
                continue
            out_source.append(source.strip().lower().split())
            out_target.append(target.strip().lower().split())
            out_align.append(alignment.strip().split())
    return list(zip(out_source, out_target, out_align))

def target_words_for_each_source_word(ss, ts, alignment):
    """Given a list of tokens in source language, a list of tokens in target
    language, and a list of cdec-style alignments of the form source-target,
    for each source word, return the string of corresponding target words."""
    alignment = [tuple(map(int, pair.split('-'))) for pair in alignment]
    outlist = [list() for i in range(len(ss))]
    indices = [list() for i in range(len(ss))]

    ## We want to get the target words in target order.
    alignment.sort(key=itemgetter(0,1))
    for (si,ti) in alignment:
        ## make sure we're grabbing contiguous phrases
        if (not indices[si]) or (ti == indices[si][-1] + 1):
            indices[si].append(ti)
            targetword = ts[ti]
            outlist[si].append(targetword)
        else:
            pass
            ## XXX: this is actually a pretty serious concern. What do?
            ## You could imagine just going like word1 <GAP> word2 ... that's
            ## what it might look like in a Hiero phrase table.
            ## This happens a lot in the bible text apparently.
            # print("warning: non-contiguous target phrase")
    # return [" ".join(targetwords) for targetwords in outlist]
    out = []
    for targetlist in outlist:
        new_tws = []
        for tw in targetlist:
            if not ispunct(tw):
                new_tws.append(tw)
        if not new_tws:
            new_tws = [UNTRANSLATED]
        out.append(" ".join(new_tws))
    assert len(out) == len(ss)
    return out

def get_target_language_sentences(triple_sentences):
    """Return all of the "sentences" over the target language, used for training
    the Source-Order language model."""
    sentences = []
    for (ss, ts, alignment) in triple_sentences:
        tws = target_words_for_each_source_word(ss, ts, alignment)
        sentence = []
        for label in tws:
            if label:
                sentence.append(label)
            else:
                sentence.append(UNTRANSLATED)
        sentences.append(sentence)
    return sentences

def ispunct(word):
    import string
    punctuations = string.punctuation + "«»¡¿—”“’‘"
    return (word in punctuations or
            all(c in punctuations for c in word))

def get_top_words(sl_sentences):
    """Take a list of sentences (each of which is a list of words), return the
    (word,count) pairs for the words appearing over a certain threshold number
    of times, ignoring punctuation and stopwords."""

    ## What if we just take all the words that occur at least 50 times?
    fd = nltk.probability.FreqDist()
    for sent in sl_sentences:
        for w in sent:
            fd[w] += 1
    mostcommon = fd.most_common()
    out = []
    for (word, count) in mostcommon:
        if word not in STOPWORDS and not ispunct(word):
            if count >= 200:
                out.append((word, count))
            else:
                break
    return out

def load_stopwords(bitextfn):
    """Determine source language from the input filename."""
    langs = bitextfn.split(".")[1]
    sl = langs.split("-")[0]
    assert sl in ["en", "es"], "wrong sl {0}".format(sl)
    sl = "english" if sl == "en" else "spanish"

    wordtext = nltk.load("corpora/stopwords/{0}".format(sl), format="text")
    wordlist = wordtext.split()

    out = set(wordlist)
    ## XXX: remove some common verbs from the set.
    out.difference_update({"estar"})
    out.difference_update({"have"})
    out.difference_update({"be"})
    out.difference_update({"do"})
    return out
