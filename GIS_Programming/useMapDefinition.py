import os, os.path, sys, tempfile
import mapnik as mapnik

map = mapnik.Map(800, 600)
# mapnik.load_map(map, "mapDefinition.xml")
mapnik.load_map(map, "map_def_basic.xml")

map.zoom_to_box(mapnik.Box2d(0, 0, 500000, 500000))
# -180.0, -90.0, 180.0, 90.0
# mapnik.render_to_file(map, ".mapCache/map.png")

scriptDir = os.path.dirname(__file__)
cacheDir = os.path.join(scriptDir, ".mapCache")
if not os.path.exists(cacheDir):
    os.mkdir(cacheDir)
fd,filename = tempfile.mkstemp(".png", dir=cacheDir)
os.close(fd)

print filename
mapnik.render_to_file(map, filename)

