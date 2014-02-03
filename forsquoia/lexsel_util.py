#!/usr/bin/env python3

import random
import sys
import xml.etree.ElementTree as ET

from util import dprint

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
        tokens.append((ref, sform, slem))
    tokens.sort()
    dprint(tokens)
    return tokens

if __name__ == "__main__": main()
