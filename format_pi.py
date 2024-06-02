#!/usr/bin/env python

#
# Format a string of digits into groups of 10 digits with
# 10 groups per line. Add a group count along the left
# margin.
#
import sys
from typing import List

digits = sys.stdin.read()

# number of digits per group
dpg : int = 10
# number of groups per line
gpl : int = 10

leading : str = ''
trailing : str = ''
[leading, trailing] = digits.split('.', 2)

prefix : str = ' ' * (len(leading)+1)

groups : List[str] = [trailing[start:start+dpg] for start in range(0, len(trailing), dpg)]

n : int = 0
groups[0] = f"{n:6}|" + leading + '.' + groups[0]
for i in range(gpl, len(groups), gpl) :
    n += gpl
    groups[i] = f"{n:6}|" + prefix + groups[i]

for i in range(0, len(groups), gpl) :
    print(" ".join(groups[i:i+10]))
