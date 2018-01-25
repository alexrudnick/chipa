"""Code for dealing with a Corpus object.

Will do basically everything that trainingdata.py does, but in a more
encapsulated way so that you can have more than one of them.

XXX: we can probably skip this whole exercise, although it would make the code
much cleaner.
"""

"""
Things that get called in trainingdata.py from other files include...

trainingdata_for(word, nonnull) -- return all the feature, label pairs in the
corpus. Assumes a particular feature set has already been loaded.
--> This is the most important function. As long as we have a Corpus object
return the same thing for trainingdata_for, we're pretty much in business.

trainingdata.load_bitext(bitextfn, alignfn) -- loads up the bitext and alignment
files for the bitext corpus

trainingdata.set_examples -- sets globals in the trainingdata module

trainingdata.set_sl_annotated -- stores all the "annotated" sentences.

So probably we should just have a big ol' list of sentences that contains
everything we care about pertaining to that sentence.
"""
