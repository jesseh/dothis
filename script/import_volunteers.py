#! /usr/bin/env python

import sys
from pprint import pprint

try:
    filename = sys.argv[1]
except IndexError:
    print("Invoke the command with the filename as an argument.")

volunteers = []
with open(filename, 'rU') as f:
    for line in f:
        parts = [part.strip() for part in line.split(',')]
        volunteers.append({'external_id': parts[0],
                           'name': " ".join(parts[1:3]),
                           'phone': parts[3]
                           })

pprint(volunteers)
