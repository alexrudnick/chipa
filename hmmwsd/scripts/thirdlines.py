#!/usr/bin/env python3

"""Print every third line of a file."""

import sys

with open(sys.argv[1]) as infile:
    for i, line in enumerate(infile):
        if i % 3 == 2: print(line.strip())
