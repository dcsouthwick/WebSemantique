#!/usr/bin/env python3
from rdflib import Graph, Namespace, RDF, Literal, BNode, RDFS, XSD, URIRef
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



def query_OSM(left, bottom, right, top):
    """ Query OSM api using box defined by edge long & lat """
    api = overpy.Overpass()
    result = api.query("node({},{},{},{});out;".format(left, bottom, right, top))
    print("Returned {} nodes, {} ways, and {} relations from OSM".format(len(result.nodes), len(result.ways), len(result.relations)))
    #data = response.json()

# https://pypi.org/project/gpxpy/
# pip3 install gpxpy rdflib --user

geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos/")
Track = URIRef("https://www.w3.org/2003/01/geo/wgs84_pos/")


graph = Graph()


def parse_gpx(gpx_file):
    """ Read in GPX xml to rdflib Graph, and export turtle """
    left_bound = 100
    bottom_bound = 100
    right_bound = 0
    top_bound = 0
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
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

                    node=BNode()
                    geo.lat=point.latitude
                    geo.long=point.longitude
                    geo.elevation=point.elevation
                    graph.add((node, RDF.type  , Literal(geo)))

                    #graph.add((node, geo.lat, Literal(geo.lat)))
                    #graph.add((node, geo.long, Literal(point.longitude)))

                    geoNumber += 1
                print("Created {0} points in RDF".format(geoNumber))
                print("Found area bounding box of {}, {}, {}, {}".format(left_bound, bottom_bound, right_bound, top_bound))
    #for waypoint in gpx.waypoints:
        #print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

    #for route in gpx.routes:
        #print('Route:')
        #for point in route.points:
            #print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
    return left_bound, bottom_bound, right_bound, top_bound


def exportGraph():
    """ Save rdfLib generated graph as turtle format for graphDB """
    #print(graph.serialize(format='turtle'))
    graph.serialize(destination="./graph.ttl", format='turtle')

#g=rdflib.Graph()
#semweb=rdflib.URIRef('http://dbpedia.org/resource/Semantic_Web')
#type=g.value(semweb, rdflib.RDFS.label)
#g.parse("GPX_Tracks/4sDDFdd4cjA.gpx", format="rdfxml")

#len(g) # prints 2

#import pprint
#for stmt in g:
#    pprint.pprint(stmt)


# Read XML file
#print(f.read())
def main():
    gpx_file = open('GPX_Tracks/4sDDFdd4cjA.gpx', 'r')
    left, bottom, right, top = parse_gpx(gpx_file)
    #exportGraph()
    query_OSM(left, bottom, right, top)

if __name__ == '__main__':
    main()
