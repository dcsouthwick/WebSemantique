import rdflib
import gpxpy
import gpxpy.gpx
# https://pypi.org/project/gpxpy/
# pip install gpxpy rdflib
from pathlib import Path, PureWindowsPath

gpx_file = open('GPX_Tracks/4sDDFdd4cjA.gpx', 'r')

gpx = gpxpy.parse(gpx_file)
for track in gpx.tracks:
    for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

for waypoint in gpx.waypoints:
    print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

for route in gpx.routes:
    print('Route:')
    for point in route.points:
        print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
#track = Path.cwd() / "GPX_Tracks" /"4sDDFdd4cjA.gpx"
#f = open(track)
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
