#!/usr/bin/env python3

## TODO(alexr): We need to get these run through the whole preprocessing
## pipeline so we can evaluate the semeval test set. 

## We need to be able to call freeling programmatically.
## And probably also cdec's tokenizer.

## XXX: magic string pointing into my files on my one particular computer.
FREELINGCONFIGDIR = "/home/alex/terere/bibletools/freeling-config"

import fileinput
from subprocess import Popen, PIPE, STDOUT

from annotated_corpus import Token

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
            token = Token(lemma, surface)
            token.annotations.add("tag=" + tag)
            sentence.append(token)
        except:
            print("surprising line:", line, lineno)
            break
    return sentence

## XXX: this assumes that Freeling is installed on the system and that we have a
## path to a directory of config files.
def run_freeling(sentence, sl):
    assert isinstance(sentence, str)
    with Popen(["analyze", "-f", FREELINGCONFIGDIR + "/" + sl + ".cfg"],
              stdout=PIPE, stdin=PIPE, stderr=STDOUT) as p:
        stdout_b = p.communicate(input=sentence.encode("utf-8"))
        stdout = stdout_b[0].decode("utf-8")
        return freeling_output_to_sentence(stdout)

def preprocess(sentence, sl):
    """Run the preprocessing pipeline on the sentence, which should be a
    string."""
    assert isinstance(sentence, str)
    return run_freeling(sentence, sl)

def main():
    for line in fileinput.input():
        line = line.strip()
        preprocessed = preprocess(line, "es")
        print(preprocessed)

if __name__ == "__main__": main()