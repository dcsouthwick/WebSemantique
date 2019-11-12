import xml.etree.ElementTree as ET

from rdflib.namespace import RDF, FOAF, RDFS, XSD, OWL
from rdflib import URIRef, BNode, Literal, Graph, Namespace, ConjunctiveGraph

# new Conjunctive Graph - the top level graph

# Create the namespace for our project

tp1 = Namespace("http://cui.unige.ch/tws/enriched_trails/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos/")
dbo = Namespace("http://dbpedia.org/ontology/")
Track1 = Graph()
# define tracks as sub graphs of our conjunctive graph (schema)
g = Graph()   # ttl output graph

g.bind("tp1", "http://cui.unige.ch/tws/enriched_trails/")
g.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos/")
g.bind("dbo", "http://dbpedia.org/ontology/")

Track = URIRef("http://cui.unige/tws/enriched_trails/Track")
Natural = URIRef("http://cui.unige/tws/tp1/Natural")
Point = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos/")
g.add((tp1.Track, RDFS.Class, RDFS.Resource))
g.add((tp1.Track, RDF.type, RDFS.Class))
g.add((tp1.Track, RDFS.range, dbo.place))

g.add((geo.SpatialThing, RDFS.subClassOf, RDFS.Resource))
g.add((geo.Point, RDFS.subClassOf, geo.SpatialThing))
g.add((geo.lat, RDFS.domain, geo.SpatialThing))
g.add((geo.long, RDFS.domain, geo.SpatialThing))
g.add((geo.alt, RDFS.domain, geo.SpatialThing))
g.add((geo.location, RDFS.range, geo.SpatialThing))

g.add((geo.Point, RDFS.domain, dbo.Place))

# http://dbpedia.org/ontology/Place
g.add((dbo.Place, RDF.type, OWL.Class))
g.add((dbo.Place, RDFS.isDefinedBy, Literal(dbo)))
g.add((dbo.Place, RDFS.domain, tp1.Track))
g.add((dbo.Place, OWL.equivalentClass, geo.Point))
g.add((dbo.Place, RDFS.domain, dbo.address))
g.add((dbo.Place, RDFS.domain, FOAF.name))

#g.add((geo.Point, RDFS. ))

#g.serialize(destination="./file.ttl", format='turtle')
print(g.serialize(format='turtle').decode('UTF-8'))

#It shall generate a rdf file like that

#@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
#@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
#@prefix xml: <http://www.w3.org/XML/1998/namespace> .
#@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

#<http://cui.unige/tws/tp1/Track> a rdfs:Class ;
    #rdfs:Class rdfs:Resource .
