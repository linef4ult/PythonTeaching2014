# mapGenerator.py

import os, os.path, sys, tempfile
import mapnik as mapnik


def generateMap(datasource, bbox, map_size, args):

    srcType = datasource['type']
    del datasource['type']

    if srcType == "OGR":
        source = mapnik.Ogr(**datasource)
    elif srcType == "PostGIS":
        source = mapnik.PostGIS(**datasource)
    elif srcType == "SQLite":
        source = mapnik.SQLite(**datasource)

    layer = mapnik.Layer("Layer")
    layer.srs = '+init=epsg:29902'
    layer.datasource = source

    map = mapnik.Map(map_size['width'], map_size['height'],
                     '+init=epsg:29902')
                     # '+proj=longlat +datum=WGS84')
    map.background = mapnik.Color(args['background'])

    style = mapnik.Style()

    rule = mapnik.Rule()
    if args['hiliteExpr'] != None:
        rule.filter = mapnik.Filter(args['hiliteExpr'])

    rule.symbols.append(mapnik.PolygonSymbolizer(
        mapnik.Color(args['hiliteFill'])))
    rule.symbols.append(mapnik.LineSymbolizer(
        mapnik.Stroke(mapnik.Color(args['hiliteLine']), 0.1)))

    style.rules.append(rule)

    rule = mapnik.Rule()
    rule.set_else(True)

    rule.symbols.append(mapnik.PolygonSymbolizer(
        mapnik.Color(args['normalFill'])))
    rule.symbols.append(mapnik.LineSymbolizer(
        mapnik.Stroke(mapnik.Color(args['normalLine']), 0.1)))

    style.rules.append(rule)
    
    map.append_style("Map Style", style)
    layer.styles.append("Map Style")
    map.layers.append(layer)

    if args['points'] != None:
        memoryDatasource = mapnik.MemoryDatasource()
        context = mapnik.Context()
        context.push("name")
        next_id = 1
        for long,lat,name in args['points']:
            wkt = "POINT (%0.8f %0.8f)" % (long,lat)
            feature = mapnik.Feature(context, next_id)
            feature['name'] = name
            feature.add_geometries_from_wkt(wkt)
            next_id = next_id + 1
            memoryDatasource.add_feature(feature)

        layer = mapnik.Layer("Points")
        layer.datasource = memoryDatasource

        style = mapnik.Style()
        rule = mapnik.Rule()

        pointImgFile = os.path.join(os.path.dirname(__file__),
                                    "point.png")

        shield = mapnik.ShieldSymbolizer(
                   mapnik.Expression('[name]'),
                   "DejaVu Sans Bold", 10,
                   mapnik.Color("#000000"),
                   mapnik.PathExpression(pointImgFile))
        shield.displacement = (0, 7)
        shield.unlock_image = True
        rule.symbols.append(shield)

        style.rules.append(rule)

        map.append_style("Point Style", style)
        layer.styles.append("Point Style")

        map.layers.append(layer)

    map.zoom_to_box(mapnik.Envelope(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']))

    scriptDir = os.path.dirname(__file__)
    cacheDir = os.path.join(scriptDir, ".mapCache")
    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)
    fd,filename = tempfile.mkstemp(".png", dir=cacheDir)
    os.close(fd)

    mapnik.render_to_file(map, filename, "png")

    return ".mapCache/" + os.path.basename(filename)


if __name__ == "__main__":


    map_parms = {}

    # datasource = {'type':'OGR', 'file':'data/TM_WORLD_BORDERS-0.3.shp','layer':'TM_WORLD_BORDERS-0.3'}
    # bbox = {'minX': -11, 'minY': 51, 'maxX': -5, 'maxY': 55}
    #
    # qry = "(select * from prgeom) as data"

    # datasource = {'type':'OGR', 'string':'PG:host=mf2.dit.ie dbname=census2011 user=stduser password=stduser',
    #               'layer_by_sql':'select * from prgeom'}

    # datasource = {'type':'OGR', 'string':'PG:host=83.212.126.59 dbname=census2011 user=student password=student',
    #               'layer_by_sql':'select * from "Provinces"'}

    datasource={'type':'PostGIS','string':'PG:host=83.212.126.59 dbname=census2011 user=student password=student','layer':'Counties'}
    bbox = {'minX': 0, 'minY': 0, 'maxX': 500000, 'maxY': 500000}


    map_size = {'width': 800, 'height': 600}
    map_parms['hiliteExpr']=None
    map_parms['background']="#8080a0"
    map_parms['hiliteLine']="#000000"
    map_parms['hiliteFill']="#408000"
    map_parms['normalLine']="#404040"
    map_parms['normalFill']="#a0a0a0"
    map_parms['points']=None



    # datasource, minX, minY, maxX, maxY,
    #             mapWidth, mapHeight,
    #             hiliteExpr=None, background="#8080a0",
    #             hiliteLine="#000000", hiliteFill="#408000",
    #             normalLine="#404040", normalFill="#a0a0a0",
    #             points=None

    # generateMap({'type':'OGR', 'file':'data/TM_WORLD_BORDERS-0.3.shp','layer':'TM_WORLD_BORDERS-0.3'}, -11, 51, -5, 55, 800, 600)

    generateMap(datasource, bbox, map_size, map_parms)
