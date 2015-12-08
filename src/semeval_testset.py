#!/usr/bin/env python3

"""
At first, let's just extract and loop over the sentences in all the *.data files
that are specified on the command line.
"""

import sys
import re
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
        out.append((lexelt, head_count, context, inst))
    return out

def head_surface_and_index(text):
    """There is a string in a <head> tag in this text -- we want to know which
    instance of that string is the one with the <head> tag; there might be more
    than one instance of that string."""
    assert "<head>" in text
    assert "</head>" in text

    needle = re.sub(r".*<head>(.*)</head>.*", "\\1", text)
    for index, match in enumerate(re.finditer(r"\b" + needle + r"\b", text)):
        curpos = match.span()[0]
        if text.find("<head>" + needle) == (curpos - len("<head>")):
            return needle, index
    assert False, "couldn't find head instance"

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
