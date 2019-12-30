#!/usr/bin/env python3
# David Southwick - UNIGE Dec 2019

from rdflib import Namespace, Graph, OWL, RDF
from rdflib.namespace import split_uri
from rdflib.term import URIRef
import urllib.parse
from pprint import pprint

g = Graph()
g.parse("/home/dsouthwi/WebSemantiquePriv/tp2/data-sources/zoo.ttl", format="turtle")

print("Running....")
# Default namespace binding - use what's already in the turtle file!
for n in g.namespaces():
    if not n[0]:
        print("using default prefix DEFAULT = {}".format(n[1]))
        DEFAULT  = Namespace(n[1])
        g.bind('', DEFAULT)
        break


def print_all():
    # print all
    for s,p,o in g.triples( (None,  None, None) ):
        print("{} {} {}".format(s,p,o))
        print()

def hasProp(prop):
    # return URI #hasProp from URI #prop
    if prop.startswith(DEFAULT['has']):
        return prop
    if prop.startswith('http'):
        hasProp = DEFAULT["has"+prop.split('#')[1].capitalize()]
        g.add((hasProp, RDF.type, OWL.ObjectProperty))
        return hasProp
    else:  
        hasProp = DEFAULT["has"+prop.capitalize()]
        g.add((hasProp, RDF.type, OWL.ObjectProperty))
        return hasProp

# Get all custom objects
objects=set()
for p in g.predicates():
    if split_uri(p)[0] != DEFAULT:
        #print("skipping {}".format(p))
        continue
    objects.add(split_uri(p)[1])
    
# Create individuals and link them
for term in objects:
#for term in {'institution', 'teamMember'}:
    for s,p,o in g.triples( (None, DEFAULT[term], None) ):
        #print("{} {} {}".format(s,p,o))
        #print("{} {} {}".format(s, hasProp(term), DEFAULT[urllib.parse.quote(o)]))
        #print("{} {} {}".format(DEFAULT[urllib.parse.quote(o)], RDF.type, DEFAULT[term]))
        g.add((DEFAULT[urllib.parse.quote(o)], RDF.type, DEFAULT[term]))
        g.add((s, hasProp(term), DEFAULT[urllib.parse.quote(o)]))
        #print(s, hasProp(term), DEFAULT[urllib.parse.quote(o)])
        g.remove((s,p,o))
        if p == DEFAULT.teamMember:
            #print("parsing person {}".format(o))
            for sub,pred,obj in g.triples (( o, None, None)):
                #print("{} {} {}".format(sub,pred,obj))
                # parse recursive statements
                if not isinstance(obj, URIRef):
                   # print("making {} instance".format(obj))
                    obj = DEFAULT[urllib.parse.quote(obj)]
                g.add((DEFAULT[sub], RDF.type, OWL.NamedIndividual))
                g.add((DEFAULT[sub], hasProp(pred), obj))
                g.add((obj, RDF.type, pred))
                #print("{} {} {}".format(obj, RDF.type, pred))
                

g.serialize(destination='zoo_parsed.ttl', format='turtle')
