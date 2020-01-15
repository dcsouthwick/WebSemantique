#!/usr/bin/env python3
# David Southwick - UNIGE Dec 2019
# This parser will read TTL and create property relationships

from rdflib import Namespace, Graph, OWL, RDF
from rdflib.namespace import split_uri
from rdflib.term import URIRef
import urllib.parse
from pprint import pprint
import os

g = Graph()
inputfiles = {'zoo.ttl', 'wpCSP.ttl', 'jrc-list'}
TTLfile = "zoo.ttl"
file_base=TTLfile.split('.')[0]
g.parse(os.getcwd()+"/data-sources/"+TTLfile, format="turtle")

print("Running on {}...".format(TTLfile))
# Default namespace binding - use what's already in the turtle file!
for n in g.namespaces():
    if not n[0]:
        print("using default prefix DEFAULT = {}".format(n[1]))
        DEFAULT  = Namespace(n[1])
        g.bind('', DEFAULT)
        break

# add helper namespace bindings!
geo = Namespace('http://www.geonames.org/ontology#')
g.bind('geo', geo)

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
# cps projects
if file_base.startswith('jrc'):
    for i in range(1,546):
        g.add((DEFAULT[f'csp-{i}'], RDF.type, DEFAULT.Project))

# Create individuals and link them
for term in objects:
#for term in {'projectName'}:
    for s,p,o in g.triples( (None, DEFAULT[term], None) ):
        #print("{} {} {}".format(s,p,o))
        #print("{} {} {}".format(s, hasProp(term), DEFAULT[urllib.parse.quote(o)]))
        #print("{} {} {}".format(DEFAULT[urllib.parse.quote(o)], RDF.type, DEFAULT[term]))
        g.remove((s,p,o))
        if not isinstance(o, URIRef):
            o = DEFAULT[urllib.parse.quote(o)]
        if term == 'area' or term == 'geographicCoverage':
                o = geo[o.split('#')[1]]
        if term == 'projectName':
            # gotcha for wpCSP
            g.add((s, RDF.type, DEFAULT["Project"]))
            g.add((o, RDF.type, DEFAULT["name"]))
            g.add((s, hasProp("name"), o))
        else:
            g.add((o, RDF.type, DEFAULT[term]))
            g.add((s, hasProp(term), o))
        #print(s, hasProp(term), o])
        
        if p == DEFAULT.teamMember:
            #print("parsing person {}".format(o))
            for sub,pred,obj in g.triples (( o, None, None)):
                # parse recursive statements
                if not isinstance(obj, URIRef):
                    obj = DEFAULT[urllib.parse.quote(obj)]
                g.add((DEFAULT[sub], RDF.type, OWL.NamedIndividual))
                g.add((DEFAULT[sub], hasProp(pred), obj))
                g.add((obj, RDF.type, pred))
                

g.serialize(destination=file_base+'-parsed.ttl', format='turtle')
print("wrote file: {}".format(file_base+'-parsed.ttl'))
