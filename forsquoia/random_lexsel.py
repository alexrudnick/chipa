#!/usr/bin/env python3

import random
import sys
import xml.etree.ElementTree as ET

from util import dprint

def make_decision(node):
    """Make a potentially-terrible decision."""
    options = [child for child in node if child.tag == 'SYN']
    choice = random.choice(options)
    ##print("options:", " ".join(opt.attrib['lem'] for opt in options))
    ##print("I have randomly chosen:", choice.attrib['lem'])
    for k,v in choice.attrib.items():
        node.attrib[k] = v
    ## remove the syn nodes.
    for option in options:
        node.remove(option)

def prettify(elem):
    from xml.dom import minidom
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'unicode')
    ## print(type(rough_string), file=sys.stderr)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_tokens(corpus):
    """Find all the nodes in the tree, return the list of source-language
    tokens."""
    target_nodes = corpus.findall(".//NODE")
    tokens = []
    for node in target_nodes:
        ref = node.attrib['ref']
        sform = node.attrib['sform']
        slem = node.attrib['slem']
        tokens.append((ref,sform, slem))
    tokens.sort()
    dprint(tokens)

def main():
    lines = []
    for line in sys.stdin:
        if line.strip():
            lines.append(line.strip())
    corpus = ET.fromstringlist(lines)

    dprint("!" * 80)
    get_tokens(corpus)
    dprint(prettify(corpus))
    dprint("!" * 80)

    ## find all the NODE elements in the tree that have a SYN underneath them
    target_nodes = corpus.findall(".//NODE/SYN/..")
    for node in target_nodes:
        make_decision(node)

    print(ET.tostring(corpus,encoding="unicode"))

if __name__ == "__main__": main()
