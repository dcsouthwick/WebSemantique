#!/usr/bin/env python3
# David Southwick - UNIGE Dec 2019

from rdflib import *
from pprint import pprint

g = Graph()
g.parse("/home/dsouthwi/WebSemantique/tp2/data-sources/zoo-small-protege.ttl", format="turtle")

print("Running....")
cui  = Namespace("http://cui.unige.ch/isi/swt/tp2c#")
g.bind('cui', cui)
#for namespace in g.namespaces():
#   print(namespace)
   #print(g.namespace_manager.normalizeUri(namespace))

# print all
def print_all():
    for s,p,o in g.triples( (None,  None, None) ):
        print("{} {} {}".format(s,p,o))
        print()


# Convert Annotation Properties into classes - grr protege ttl importing
for s,p,o in g.triples( (None,  RDF.type, OWL.AnnotationProperty) ):
    #print("{} was a {}".format(s,o))
    g.set((s,p,OWL.Class))

print()
# Generate Object Properties
# http://cui.unige.ch/isi/swt/tp2c#Description a http://www.w3.org/2002/07/owl#Class
for s,p,o in g.triples( (None,  RDF.type, OWL.Class) ):
   newProp = cui["has"+s.split('#')[1].capitalize()]
   #print("{}, {}, {}".format(newProp,p,OWL.ObjectProperty))
   g.add((newProp, RDF.type, OWL.ObjectProperty))

# Create individuals and link them
for s,p,o in g.triples( (None, cui.category, None) ):
    print("{} {} {}".format(s, cui.hasCategory, cui[o]))
    g.add((s,cui.hasCategory, cui[o]))
    g.set((cui[o], RDF.type, cui.category))
    g.remove((s,p,o))

for s,p,o in g.triples( (None, cui.desc, None) ):
    print("{} {} {}".format(s,p,o))
    print("{} {} {}".format(s, cui.hasDesc, cui[o.replace(" ", "_")]))
    g.add((s,cui.hasDesc, cui[o.replace(" ", "_")]))
    g.set((cui[o.replace(" ", "_")], RDF.type, cui.desc))
    g.remove((s,p,o))

# TODO: Generalize above steps for all predicates

# print( g.serialize(format='turtle'))
g.serialize(destination='zoo_parsed.ttl', format='turtle')