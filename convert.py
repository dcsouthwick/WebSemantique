
import rdflib
from rdflib import Graph, Namespace, RDF, Literal, BNode, RDFS, XSD, URIRef
#import sparqlwrapper
import gpxpy
import gpxpy.gpx
import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
osm_query="https://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145"
overpass_query = """
[out:json];
node ["amenity"="fuel
(21.215460, -157.956619, 21.385951, -157.724533);
out;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
#data = response.json()

# https://pypi.org/project/gpxpy/
# pip3 install gpxpy rdflib --user

geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos/")
Track = URIRef("https://www.w3.org/2003/01/geo/wgs84_pos/")


graph = Graph()

def parse_gpx(gpx_file):
    left_bound = 100
    bottom_bound = 100
    right_bound = 0
    top_bound = 0
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
                geoNumber = 0
                for point in segment.points:
                    print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
                    # get bounding area from track
                    if point.longitude < left_bound:
                        left_bound=point.longitude
                    if point.latitude < bottom_bound:
                        bottom_bound = point.latitude
                    if point.longitude > right_bound:
                        right_bound = point.longitude
                    if point.latitude > top_bound:
                        top_bound = point.latitude

                    node=BNode()
                    geo.lat=point.latitude
                    geo.long=point.longitude
                    geo.elevation=point.elevation
                    graph.add((node, RDF.type  , Literal(geo)))

                    #graph.add((node, geo.lat, Literal(geo.lat)))
                    #graph.add((node, geo.long, Literal(point.longitude)))

                    geoNumber += 1
                print("Created {0} points in RDF".format(geoNumber))
                print("Found area bounding box of {},{},{},{}".format(left_bound, bottom_bound, right_bound, top_bound))
    for waypoint in gpx.waypoints:
        print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

    for route in gpx.routes:
        print('Route:')
        for point in route.points:
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

def printGraph():
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
    print("python main function")
    parse_gpx(gpx_file)
    printGraph()

if __name__ == '__main__':
    main()
