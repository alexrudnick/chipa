# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the TreeTagger POS-tagger
#
# Copyright (C) Mirko Otto
# Author: Mirko Otto <dropsy@gmail.com>

"""
A Python module for interfacing with the Treetagger by Helmut Schmid.
"""

import os
from subprocess import Popen, PIPE

from nltk.internals import find_binary, find_file
from nltk.tag.api import TaggerI

_treetagger_url = 'http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger'

_treetagger_languages = {
'latin-1':['bulgarian', 'english', 'estonian', 'french', 'german', 'greek', 'italian', 'latin', 'russian', 'spanish', 'swahili'],
'utf8' : ['french', 'german', 'greek', 'italian', 'spanish', 'dutch']}

"""The default encoding used by TreeTagger: utf8. '' means latin-1; ISO-8859-1"""
_treetagger_charset = ['utf8', 'latin-1']

class TreeTagger(TaggerI):
    r"""
    A class for pos tagging with TreeTagger. The input is the paths to:
     - a language trained on training data
     - (optionally) the path to the TreeTagger binary
     - (optionally) the encoding of the training data (default: utf8)

    This class communicates with the TreeTagger binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger(encoding='latin-1',language='english')
        >>> tt.tag('What is the airspeed of an unladen swallow ?')
        [['What', 'WP', 'What'],
         ['is', 'VBZ', 'be'],
         ['the', 'DT', 'the'],
         ['airspeed', 'NN', 'airspeed'],
         ['of', 'IN', 'of'],
         ['an', 'DT', 'an'],
         ['unladen', 'JJ', '<unknown>'],
         ['swallow', 'NN', 'swallow'],
         ['?', 'SENT', '?']]

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger()
        >>> tt.tag('Das Haus ist sehr schön und groß. Es hat auch einen hübschen Garten.')
        [['Das', 'ART', 'die'],
         ['Haus', 'NN', 'Haus'],
         ['ist', 'VAFIN', 'sein'],
         ['sehr', 'ADV', 'sehr'],
         ['schön', 'ADJD', 'schön'],
         ['und', 'KON', 'und'],
         ['groß', 'ADJD', 'groß'],
         ['.', '$.', '.'],
         ['Es', 'PPER', 'es'],
         ['hat', 'VAFIN', 'haben'],
         ['auch', 'ADV', 'auch'],
         ['einen', 'ART', 'eine'],
         ['hübschen', 'ADJA', 'hübsch'],
         ['Garten', 'NN', 'Garten'],
         ['.', '$.', '.']]
    """

    def __init__(self, path_to_home=None,
                 tt_home=None,
                 language='german', 
                 encoding='utf8', verbose=False):
        """
        Initialize the TreeTagger.

        :param path_to_home: The TreeTagger binary.
        :param language: Default language is german.
        :param encoding: The encoding used by the model. Unicode tokens
            passed to the tag() and batch_tag() methods are converted to
            this charset when they are sent to TreeTagger.
            The default is utf8.

            This parameter is ignored for str tokens, which are sent as-is.
            The caller must ensure that tokens are encoded in the right charset.
        """
        treetagger_paths = ['.', '/usr/bin', '/usr/local/bin', '/opt/local/bin',
                        '/Applications/bin', '~/bin', '~/Applications/bin',
                        '~/work/TreeTagger/cmd']
        treetagger_paths = list(map(os.path.expanduser, treetagger_paths))
        if tt_home:
            treetagger_paths.append(tt_home)

        try:
            if language in _treetagger_languages[encoding]:
                if encoding == 'latin-1':
                    """the executable has no encoding information for latin-1"""
                    treetagger_bin_name = 'tree-tagger-' + language
                    self._encoding = 'latin-1'
                else:
                    treetagger_bin_name = 'tree-tagger-' + language + '-' + encoding
                    self._encoding = encoding

            else:
                raise LookupError('NLTK was unable to find the TreeTagger bin!')
        except KeyError as e:
                raise LookupError('NLTK was unable to find the TreeTagger bin!')

        self._treetagger_bin = find_binary(
                treetagger_bin_name, path_to_home,
                env_vars=('TREETAGGER', 'TREETAGGER_HOME'),
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)

        if encoding in _treetagger_charset:
            self._encoding = encoding
        
    def tag(self, sentence):
        """Tags a single sentence: a list of words.
        The tokens should not contain any newline characters.
        """
        encoding = self._encoding

        # Write the actual sentence to the temporary input file
        if isinstance(sentence, list):
            _input = '\n'.join((x for x in sentence))
        else:
            _input = sentence

        if isinstance(_input, str) and encoding:
            _input = _input.encode(encoding)

        # Run the tagger and get the output
        p = Popen([self._treetagger_bin], 
                    shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        (stdout, stderr) = p.communicate(_input)
        assert type(stdout) == bytes
        treetagger_output = stdout.decode(encoding)

        # Check the return code.
        if p.returncode != 0:
            print(stderr)
            raise OSError('TreeTagger command failed!')

        ## if isinstance(stdout, str) and encoding:
        ##     treetagger_output = stdout.decode(encoding)
        ## else:
        ##     treetagger_output = tUoB(stdout)

        # Output the tagged sentence
        tagged_sentence = []
        for tagged_word in treetagger_output.strip().split('\n'):
            tagged_word_split = tagged_word.split('\t')
            tagged_sentence.append(tagged_word_split)

        return tagged_sentence

    def batch_tag(self, sentences):
        """Tags a list of sentences: a list of list of words.
        The tokens should not contain any newline characters.
        Will return a list of list of [word,tag,lemma].
        """
        encoding = self._encoding

        sentence_chunks = []
        sentence_lengths = list(map(len, sentences))
        for sentence in sentences:
            for i,token in enumerate(sentence):
                assert '\t' not in token
            chunk = '\n'.join((token for token in sentence))
            chunk += '\n'
            sentence_chunks.append(chunk)
        _input = '\n'.join(sentence_chunks)

        if isinstance(_input, str) and encoding:
            _input = _input.encode(encoding)

        # Run the tagger and get the output
        p = Popen([self._treetagger_bin], 
                    shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        (stdout, stderr) = p.communicate(_input)
        assert type(stdout) == bytes
        treetagger_output = stdout.decode(encoding)

        # Check the return code.
        if p.returncode != 0:
            print(stderr)
            raise OSError('TreeTagger command failed!')

        ## if isinstance(stdout, str) and encoding:
        ##     treetagger_output = stdout.decode(encoding)
        ## else:
        ##     treetagger_output = tUoB(stdout)

        # Output the tagged sentences
        all_the_output = []
        for tagged_word in treetagger_output.strip().split('\n'):
            if '\t\t' in tagged_word:
                print("wtf:", str(tagged_word))
                tagged_word = tagged_word.replace('\t\t', '\t')
            tagged_word_split = tagged_word.split('\t')
            all_the_output.append(tagged_word_split)

        total_token_count = 0
        for sentlen in sentence_lengths:
            total_token_count += sentlen
        ## print(len(all_the_output), total_token_count)

        tagged_sentences = []
        cur_pos = 0
        for sent in sentences:
            sent_len = len(sent)
            tagged_sentences.append(all_the_output[cur_pos:cur_pos+sent_len])
            cur_pos += sent_len

        output_lengths = list(map(len, tagged_sentences))
        ## for sent,out in zip(sentences, tagged_sentences):
        ##     print("sent:", sent)
        ##     print("out lemmas:", [tup[2] for tup in out])
        assert len(all_the_output) == total_token_count
        assert sentence_lengths == output_lengths
        return tagged_sentences

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
