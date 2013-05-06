#!/usr/bin/env python3

import functools
from nltk.tag.stanford import POSTagger

taggerhome = None

@functools.lru_cache(maxsize=20)
def get_tagger():
    assert taggerhome
    ## these need to be environment variables or commandline arguments.
    tagger = taggerhome + '/models/wsj-0-18-bidirectional-distsim.tagger'
    jar = taggerhome + '/stanford-postagger.jar'
    stanford_tagger = POSTagger(tagger, jar, encoding='utf8',
                                java_options='-mx8192m')
    return stanford_tagger
