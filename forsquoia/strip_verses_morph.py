#!/usr/bin/env python3

"""The Bible files we've got have a bunch of stray line number tags in there.
Strip those out."""

import re
import fileinput

pat = re.compile(r"99\d.*\t99\d.*\t[+][?]")

for line in fileinput.input():
    line = line.strip()
    if line == "[\t[[$.]": continue
    if line == "]\t][$.]": continue
    if pat.match(line): continue
    print(line)
