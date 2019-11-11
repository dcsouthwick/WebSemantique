import xml.etree.ElementTree as ET

from rdflib.namespace import RDF, FOAF, RDFS, XSD
from rdflib import URIRef, BNode, Literal, Graph, Namespace

n = Namespace("http://cui.unige.ch/tws/tp1/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
g = Graph()   # ttl output graph
Track = URIRef("http://cui.unige/tws/tp1/Track")
Natural = URIRef("http://cui.unige/tws/tp1/Natural")
g.add((n.Track, RDFS.Class, RDFS.Resource))
g.add((n.Track, RDF.type, RDFS.Class))
g.add((n.Track, RDFS.range, geo.Point))
g.add((geo.Point, ))

#g.serialize(destination="./file.ttl", format='turtle')
print(g.serialize(format='turtle').decode('UTF-8'))

#It shall generate a rdf file like that

#@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
#@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
#@prefix xml: <http://www.w3.org/XML/1998/namespace> .
#@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#<http://cui.unige/tws/tp1/Track> a rdfs:Class ;
    #rdfs:Class rdfs:Resource .
