import untangle
from pathlib import Path, PureWindowsPath

data_folder = Path('C:/Users/dcsou/Documents/GPX_Tracks/GPX_Tracks')
track = data_folder / "4sDDFdd4cjA.gpx"
f = open(track)


# Read XML file
#print(f.read())

obj = untangle.parse(track)
