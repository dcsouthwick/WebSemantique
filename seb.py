#import xml.etree.ElementTree as ET

from rdflib.namespace import RDF, FOAF, RDFS, XSD, OWL
from rdflib import URIRef, BNode, Literal, Graph, Namespace, ConjunctiveGraph

# new Conjunctive Graph - the top level graph

# Create the namespace for our project

tp1 = Namespace("http://cui.unige.ch/tws/enriched_trails/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos/")
dbo = Namespace("http://dbpedia.org/ontology/")
schema = Namespace("https://schema.org/")
# define tracks as sub graphs of our conjunctive graph (schema)
g = Graph()   # ttl output graph

g.bind("tp1", "http://cui.unige.ch/tws/enriched_trails/")
g.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos/")
g.bind("dbo", "http://dbpedia.org/ontology/")
g.bind("schema", "https://schema.org/")
# defind terms in our custom namespace
Track = URIRef("http://cui.unige/tws/enriched_trails/Track")
Place = URIRef("http://cui.unige/tws/enriched_trails/Place")
g.add((tp1.Track, RDFS.subClassOf, RDFS.Resource))
g.add((tp1.Track, RDF.type, RDFS.Class))
g.add((tp1.Track, RDFS.range, tp1.Place))

g.add((geo.SpatialThing, RDFS.subClassOf, RDFS.Resource))
g.add((geo.Point, RDFS.subClassOf, geo.SpatialThing))
g.add((geo.lat, RDFS.domain, geo.SpatialThing))
g.add((geo.long, RDFS.domain, geo.SpatialThing))
g.add((geo.alt, RDFS.domain, geo.SpatialThing))
g.add((geo.location, RDFS.range, geo.SpatialThing))

g.add((geo.Point, RDFS.domain, tp1.Place))

# http://dbpedia.org/ontology/Place
g.add((tp1.Place, RDF.type, OWL.Class))
g.add((tp1.Place, OWL.equivalentClass, schema.Place))
g.add((tp1.Place, RDFS.domain, tp1.Track))
g.add((tp1.Place, RDF.Property, geo.Point))
g.add((tp1.Place, RDF.Property, schema.address))
g.add((tp1.Place, RDF.langString, tp1.label))
g.add((tp1.Place, RDFS.label, tp1.label))

node = BNode()
g.add((node, RDF.type, geo.Point))
lat='45'
print(type(lat))
g.add((node, geo.lat, Literal(lat, datatype=XSD.string)))


#g.add((geo.Point, RDFS. ))

g.serialize(destination="./file.ttl", format='turtle')
print(g.serialize(format='turtle').decode('UTF-8'))
