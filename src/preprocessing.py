#!/usr/bin/env python3

## TODO(alexr): We need to get these run through the whole preprocessing
## pipeline so we can evaluate the semeval test set. 

## We need to be able to call freeling programmatically.
## And probably also cdec's tokenizer.

## XXX: magic string pointing into my files on my one particular computer.

import fileinput
import functools
from subprocess import Popen, PIPE, STDOUT
import os

from annotated_corpus import Token

home = os.path.expanduser("~")
FREELINGCONFIGDIR = home + "/terere/bibletools/freeling-config"

def freeling_output_to_sentence(freeling_output):
    """Return a list of tokens. We should only be given a single sentence at
    once."""
    sentence = []
    lines = freeling_output.split("\n")
    lemmas = []
    lineno = 0
    for i, line in enumerate(lines):
        lineno += 1
        line = line.strip()
        if sentence and not line:
            assert ("" == line.strip() for line in lines[i:])
            return sentence
        # sirvan servir VMSP3P0 0.885892
        try:
            ## There can actually be more than the first four fields.
            ## But we just take the first four.
            surface, lemma, tag, confidence = line.split()[:4]
            print("lemma", lemma)
            token = Token(lemma, surface)
            token.annotations.add("tag=" + tag)
            sentence.append(token)
        except:
            print("surprising line:", line, lineno)
            break
    return sentence

## XXX: this assumes that Freeling is installed on the system and that we have a
## path to a directory of config files.
def run_freeling(sentence, sl, tokenize):
    assert isinstance(sentence, str)

    command = ["analyze", "-f", FREELINGCONFIGDIR + "/" + sl + ".cfg"]
    if not tokenize:
        command.extend(["--inplv", "splitted", "--input", "freeling"])
        tokens = sentence.split(' ')
        sentence = '\n'.join(tokens)

    with Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
        stdout_b = p.communicate(input=sentence.encode("utf-8"))
        stdout = stdout_b[0].decode("utf-8")
        print("stdout", stdout)
        return freeling_output_to_sentence(stdout)

@functools.lru_cache(maxsize=100000)
def preprocess(sentence, sl, tokenize=True):
    """Run the preprocessing pipeline on the sentence, which should be a
    string."""
    assert isinstance(sentence, str)
    return run_freeling(sentence, sl, tokenize=tokenize)

def main():
    for line in fileinput.input():
        line = line.strip()
        preprocessed = preprocess(line, "es")
        print(preprocessed)

if __name__ == "__main__": main()
