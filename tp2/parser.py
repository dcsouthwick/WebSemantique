#!/usr/bin/env python3

import rdflib
import pprint

g = rdflib.Graph()
g.parse("data-sources/zoo.ttl", format="turtle")

print("Running....")

for s,p,o in g:
    print((s,p,o))
    print("")
    print("")