#!/usr/bin/env python3

import random
import sys
import xml.etree.ElementTree as ET
import xmlrpc.client

from util import dprint
import lexsel_util

def make_decision(node, answers):
    """Make a potentially-terrible decision."""
    ref = int(node.attrib['ref'])
    chipa_says = answers[ref - 1]

    choice = None

    if chipa_says not in ["<OOV>", "<untranslated>"]:
        for child in node:
            if child.tag == "SYN" and child.attrib['lem'] == chipa_says:
                choice = child
    if not choice:
        dprint("CLASSIFIER DIDN'T HELP, BAILING")
        return

    dprint("HOLY COW CLASSIFIER MADE A DECISION")
    for k,v in choice.attrib.items():
        node.attrib[k] = v
    ## remove the syn nodes.
    for option in options:
        node.remove(option)

def main():
    s = xmlrpc.client.ServerProxy('http://localhost:8000')

    lines = []
    for line in sys.stdin:
        if line.strip():
            lines.append(line.strip())
    corpus = ET.fromstringlist(lines)

    for sentence in corpus:
        tuples = lexsel_util.get_tuples(sentence)
        answers = s.label_sentence(tuples)
        dprint(answers)
        ## all the NODE elements in the tree that have a SYN underneath
        target_nodes = sentence.findall(".//NODE/SYN/..")
        for node in target_nodes:
            make_decision(node, answers)

    print(ET.tostring(corpus,encoding="unicode"))

if __name__ == "__main__": main()
