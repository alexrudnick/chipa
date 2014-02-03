#!/usr/bin/env python3

import random
import sys
import xml.etree.ElementTree as ET

from util import dprint
import lexsel_util

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

def main():
    lines = []
    for line in sys.stdin:
        if line.strip():
            lines.append(line.strip())
    corpus = ET.fromstringlist(lines)

    dprint("!" * 80)
    lexsel_util.get_tokens(corpus)
    dprint(lexsel_util.prettify(corpus))
    dprint("!" * 80)

    ## find all the NODE elements in the tree that have a SYN underneath them
    target_nodes = corpus.findall(".//NODE/SYN/..")
    for node in target_nodes:
        make_decision(node)

    print(ET.tostring(corpus,encoding="unicode"))

if __name__ == "__main__": main()
