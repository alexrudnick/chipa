#!/usr/bin/env python3

"""
At first, let's just extract and loop over the sentences in all the *.data files
that are specified on the command line.
"""

import sys
import argparse
from xml.sax import handler, make_parser

class SentenceExtractor(handler.ContentHandler):
    def __init__(self):
        self.sentences = []
        self.instance_id = None
        self.cur_sentence = ""
        self.lexelt = None
        self.in_context = False
        self.head_count = 0

    def characters(self, content):
        # print("characters", content)
        if self.in_context:
            self.cur_sentence += content

    def startElement(self, name, attrs):
        if name == "lexelt":
            self.lexelt = attrs.get("item")

        if name == "instance":
            self.instance_id = attrs.get("id")
            self.cur_sentence = ""
            self.head_count = 0

        if name == "context":
            self.in_context = True

        if name == "head":
            self.cur_sentence += "<head>"
            self.head_count += 1


    def endElement(self, name):
        if name == "context":
            self.in_context = False
            self.sentences.append((self.lexelt,
                                   self.head_count,
                                   self.cur_sentence,
                                   self.instance_id))

        if name == "head":
            self.cur_sentence += "</head>"

def extract_wsd_problems(fn):
    handler = SentenceExtractor()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(fn)

    out = []
    for (lexelt, head_count, context, inst) in list(handler.sentences):
        ## problem = WSDProblem(lexelt, context, instance_id=inst, testset=True)
        ##out.append(problem)
        print(lexelt, head_count, context, inst)
        out.append((lexelt, head_count, context, inst))
    ## sents = [problem.tokenized for problem in out]
    ## tagger = stanford.get_tagger()
    ## tagged_sents = tagger.batch_tag(sents)
    ## assert len(tagged_sents) == len(out)
    ## for tagged_sent,problem in zip(tagged_sents, out):
    ##     problem.tagged = tagged_sent
    ## print("tagged.")
    return out

def main():
    parser = argparse.ArgumentParser(description='clwsd')
    parser.add_argument('--problems', type=str, required=True)
    args = parser.parse_args()
    fn = args.problems

    problems = extract_wsd_problems(fn)
    for problem in problems:
        print("***")
        print(problem)

if __name__ == "__main__": main()
