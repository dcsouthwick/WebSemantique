#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rdflib import Graph, Namespace, RDF, Literal, BNode, RDFS, XSD, URIRef, OWL

#import sparqlwrapper
import gpxpy
import gpxpy.gpx
import requests
import json
import overpy
# https://python-overpy.readthedocs.io/en/latest/example.html
########################
#
# Usage: python3 convert.py
# NB: requires course .gpx files in ./GPX_Tracks/*
########################

# Create the namespace for our project
tp1 = Namespace("http://cui.unige.ch/tws/enriched_trails/")
geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos/")
dbo = Namespace("http://dbpedia.org/ontology/")
schema = Namespace("https://schema.org/")
# define tracks as sub graphs of our conjunctive graph (schema)
graph = Graph()   # ttl output graph

graph.bind("tp1", "http://cui.unige.ch/tws/enriched_trails/")
graph.bind("geo", "http://www.w3.org/2003/01/geo/wgs84_pos/")
graph.bind("dbo", "http://dbpedia.org/ontology/")
graph.bind("schema", "https://schema.org/")
# define terms in our custom namespace
Track = URIRef("http://cui.unige/tws/enriched_trails/Track")
Place = URIRef("http://cui.unige/tws/enriched_trails/Place")

def initializeGraph():
    """ Initialize and construct ontology """
    graph.add((tp1.Track, RDFS.subClassOf, RDFS.Resource))
    graph.add((tp1.Track, RDF.type, RDFS.Class))
    graph.add((tp1.Track, RDFS.range, tp1.Place))

    graph.add((geo.SpatialThing, RDFS.subClassOf, RDFS.Resource))
    graph.add((geo.Point, RDFS.subClassOf, geo.SpatialThing))
    graph.add((geo.lat, RDFS.domain, geo.SpatialThing))
    graph.add((geo.long, RDFS.domain, geo.SpatialThing))
    graph.add((geo.alt, RDFS.domain, geo.SpatialThing))
    graph.add((geo.location, RDFS.range, geo.SpatialThing))

    graph.add((geo.Point, RDFS.domain, tp1.Place))

    # http://dbpedia.org/ontology/Place
    graph.add((tp1.Place, RDF.type, OWL.Class))
    graph.add((tp1.Place, OWL.equivalentClass, schema.Place))
    graph.add((tp1.Place, RDFS.domain, tp1.Track))
    graph.add((tp1.Place, RDFS.range, geo.Point))
    graph.add((tp1.Place, RDF.Property, schema.address))
    graph.add((tp1.Place, RDF.langString, tp1.label))
    graph.add((tp1.Place, RDFS.label, tp1.label))


def query_OSM(left, bottom, right, top):
    """ Query OSM api using box defined by edge long & lat """
    api = overpy.Overpass()
    result = api.query("way({},{},{},{})[\"name\"][!\"highway\"];out geom;".format(left, bottom, right, top))
    print("Returned {} nodes, {} ways, and {} relations from OSM".format(len(result.nodes), len(result.ways), len(result.relations)))
    #data = response.json()
    #for node in result.nodes:
        #graph.add()


def parse_gpx(gpx_file):
    """ Read in GPX xml to rdflib Graph, and export turtle """
    left_bound = 100
    bottom_bound = 100
    right_bound = 0
    top_bound = 0
    prefix = 'GPX_Tracks/'
    gpx = gpxpy.parse(open(prefix+gpx_file, 'r'))
    for track in gpx.tracks:
        trackIdent = URIRef("http://cui.unige.ch/tws/enriched_trails/"+gpx_file)
        graph.add((trackIdent, RDF.type, tp1.Track))
        for segment in track.segments:
                geoNumber = 0
                for point in segment.points:
                    #print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
                    # get bounding area from track
                    if point.latitude < left_bound:
                        left_bound=point.latitude
                    if point.longitude < bottom_bound:
                        bottom_bound = point.longitude
                    if point.latitude > right_bound:
                        right_bound = point.latitude
                    if point.longitude > top_bound:
                        top_bound = point.longitude

                    # create point in graph
                    node = BNode()
                    graph.add((node, RDF.type, geo.Point))
                    graph.add((node, geo.lat, Literal(str(point.latitude))))
                    graph.add((node, geo.long, Literal(str(point.longitude))))
                    graph.add((node, geo.alt, Literal(str(point.elevation))))

                    geoNumber += 1
                print("Created {0} points in RDF".format(geoNumber))
                print("Found area bounding box of {}, {}, {}, {}".format(left_bound, bottom_bound, right_bound, top_bound))
    for waypoint in gpx.waypoints:
        print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
        wpt = BNode()
        graph.add((wpt, RDF.type, tp1.Place))
        graph.add((wpt, RDFS.label, Literal(str(waypoint.name))))
        graph.add((wpt, geo.lat, Literal(str(waypoint.latitude))))
        graph.add((wpt, geo.long, Literal(str(waypoint.longitude))))

    for route in gpx.routes:
        print('Route:')
        for point in route.points:
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
    return left_bound, bottom_bound, right_bound, top_bound


def exportGraph():
    """ Save rdfLib generated graph as turtle format for graphDB """
    #print(graph.serialize(format='turtle'))
    print(graph.serialize(format='turtle').decode('UTF-8'))
    graph.serialize(destination="./graph.ttl", format='turtle')


def main():
    initializeGraph()
    gpx_file = '4sDDFdd4cjA.gpx'
    left, bottom, right, top = parse_gpx(gpx_file)
    exportGraph()
    query_OSM(left, bottom, right, top)

if __name__ == '__main__':
    main()
