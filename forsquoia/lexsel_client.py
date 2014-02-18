#!/usr/bin/env python3

import random
import sys
import xml.etree.ElementTree as ET
import xmlrpc.client

from util import dprint
import lexsel_util

def make_decision(node, answers):
    """Make a potentially-terrible decision."""
    default = node.attrib['lem']
    option_nodes = [child for child in node if child.tag == 'SYN']
    option_lemmas = ([opt.attrib['lem'] for opt in option_nodes] +
                     [default])

    dprint("[DEFAULT]", default)
    dprint("[OPTIONS]", " ".join(option_lemmas))

    textref = node.attrib['ref']
    try:
        ref = int(textref)
    except:
        dprint("REFISNOTINT:", textref)
        ref = int(float(textref))
        
    chipa_says = answers[ref - 1]
    dprint("[CHIPASAYS]", chipa_says)

    ## chipa_says is the list of things in descending order of goodness.
    best = None
    for ans in chipa_says:
        if ans in option_lemmas:
            best = ans
            break

    choice = None
    for child in option_nodes:
        if child.attrib['lem'] == best:
            dprint("HOLY COW CLASSIFIER MADE A DECISION")
            choice = child
            break
    if choice is None:
        dprint("CLASSIFIER DIDN'T HELP, BAILING")
        return True

    for k,v in choice.attrib.items():
        node.attrib[k] = v
    ## remove the syn nodes.
    for option_node in option_nodes:
        node.remove(option_node)
    return True

def main():
    s = xmlrpc.client.ServerProxy('http://localhost:8000')

    lines = []
    for line in sys.stdin:
        if line.strip():
            lines.append(line.strip())
    corpus = ET.fromstringlist(lines)

    for sentence in corpus:
        sentnum = sentence.attrib['ref']
        tuples = lexsel_util.get_tuples(sentence)
        surface = [tup[1] for tup in tuples]
        dprint("[SURFACE]", " ".join(surface))
        answers = s.label_sentence(tuples)
        dprint("[ANSWERS]", answers)
        ## all the NODE elements in the tree that have a SYN underneath
        target_nodes = sentence.findall(".//NODE/SYN/..")
        changed = False
        for node in target_nodes:
            changed_here = make_decision(node, answers)
            if changed_here:
                changed = True
        if changed:
            dprint("[CLASSIFIERSENTENCE]", sentnum)

    print(ET.tostring(corpus,encoding="unicode"))

if __name__ == "__main__": main()
