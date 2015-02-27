"""
Basic spatial analysis using vector data and appropriate libraries
The task

Take a data set of "populated places" from the PostgreSQL/PostGIS server on 83.212.126.59 and the geometry of Cork from
the "Counties" shapefile and return a list of settlements in Cork sorted by population size. Also, find the postal address
of the centroid of Cork County.

Data sources

Connection string for database: "dbname=census2011 user=student password=student host=83.212.126.59 port=5432"
Database query: "SELECT * FROM geonames_populated"

Counties shapefile:
http://83.212.126.59:8080/geoserver/dit-wmap/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dit-wmap:Counties&outputFormat=SHAPE-ZIP

Libraries

    Database access: psycopg
    Shapefile handling: fiona
    Projection transformation: pyproj
    String processing: string
    Address geocoding: geopy
    Geometry operations: shapely

Points to note

    Populated places data and county geometries are in different coordinate refeences. This will have to be normalised.
    The solution to this is to convert the populated places points from WGS84 (EPSG 4326) to Irish Grid (EPSG 29902).
    Geocoding needs data to be in WGS84.
    The geometry of Cork has two components, Cork City and Cork County. These will have to be merged.
"""

__author__ = 'mark'

from os import path
import psycopg2
import psycopg2.extras
import fiona
from shapely.geometry import Point, mapping, shape
from shapely.ops import cascaded_union
import pyproj
import geopy
from geopy.geocoders import Nominatim

OUTPUT_DIR = ".cache"

def get_db_data(conn_string, db_query):
    """
    Makes a connection to a PostgreSQL database and creates a cursor representing a collection of rows. The elements in
    these rows can be accessed by numeric index or column name.

    :return: List of rows representing query result set.
    """

    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(db_query)
            c = cur.fetchall()
            cur.close()
            return c
        except psycopg2.Error as e:
            print(e)
            return None

    except psycopg2.OperationalError as e:
        print(e)
        return None


def transform_coordinates(source_srid, target_srid, source_x, source_y):
    """
    Transforms a coordinate pair from one spatial reference system to another. Inputs are the EPSG reference codes for
    source and target SRIDs in the format "epsg:nnn" where nnn is the numeric code. Examples are 4326 (WGS84) and 29902
    (Irish Grid).

    Source x and y could be lon/lat or easting/northing

    :param source_srid:
    :param target_srid:
    :param source_x:
    :param source_y:
    :return: tuple containing new coordinate pair
    """

    try:
        source_proj = pyproj.Proj(init=source_srid)
        target_proj = pyproj.Proj(init=target_srid)

        target_x, target_y = pyproj.transform(source_proj, target_proj, source_x, source_y)

        return (target_x, target_y)

    except RuntimeError as e:
        print(str(e))
        return None


def geocode_item(**kwargs):
    """
    Geocode address or reverse geocode coordinate pair using OSM's Nominatim geocoder.

    :param kwargs: Dictionary of key/value pairs which vary depending on specific requirements. To geocode an address
    you need to supply an "address" item. To reverse geocode a coordinate pair, you need to supply a lat/lon pair and
    have the "reverse" item set to true. In either case, the coordinate pair must be in WGS84.

    :return: A dictionary of result key/value pairs
    """

    try:
        geolocator = Nominatim()
        if (not kwargs["reverse"]) and kwargs["address"]:
            location = geolocator.geocode(kwargs["address"])
            return location.raw
        elif (kwargs["reverse"]) and (kwargs["lon"] and kwargs["lat"]):
            location = geolocator.reverse((kwargs["lat"], kwargs["lon"]))
            return location.raw
        else:
            return None
    except geopy.exc.GeopyError as e:
        print(str(e))
        return None


def create_merged_geom(shapefile, filter_key, filter_value):
    """
    Creates a geometry object from a shapefile representing the merged geometries of one or more features based on
    filter parameters

    :param shapefile: Shapefile containing features to be merged
    :param filter_key: Attribute name. We want to merge based on the contents of this.
    :param filter_value: Value of attribute (above). If we get a natch we include this feature in the merge
    :return:
    """

    merged_shp = path.join(OUTPUT_DIR, "merged_geom.shp")

    try:
        with fiona.open(shapefile, "r", encoding="utf-8") as input:
            schema = input.schema.copy()
            output_schema = {'geometry': schema["geometry"], 'properties': {'name': 'str'}}

            with fiona.open(merged_shp, "w", driver=input.driver, schema=output_schema, crs=input.crs, encoding=input.encoding) as output:
                shapes = []

                for feature in input:
                    if filter_value.lower() in feature["properties"][filter_key].lower():
                        shapes.append(shape(feature['geometry']))

                merged = cascaded_union(shapes)

                output.write({
                    'properties': {
                        'name': filter_value.title()
                    },
                    'geometry': mapping(merged)
                })

        return merged

    except Exception as e:
        print(str(e))
        return None


def main():
    #
    # Set up constants
    #
    DB_CONN_STRING = "dbname=census2011 user=student password=student host=83.212.126.59 port=5432"
    DB_QUERY = "SELECT * FROM geonames_populated"
    SHAPEFILE = "/home/mark/Downloads/counties/Counties.shp"

    #
    # Get database data
    #
    populated_places_dataset = get_db_data(DB_CONN_STRING, DB_QUERY)

    #
    # Merge shapefiles
    #
    merged = create_merged_geom(SHAPEFILE, "countyname", "cork")

    #
    #  Reverse geocode centroid of county
    #
    centroid = merged.centroid
    centroid_lon, centroid_lat = transform_coordinates("epsg:29902", "epsg:4326", centroid.x, centroid.y)
    centroid_address = geocode_item(reverse=True, lat=centroid_lat, lon=centroid_lon)
    centroid_address = centroid_address["display_name"]

    #
    #  Create point-in-poly list
    #
    places_list = []

    for place in populated_places_dataset:
        if place["population"] > 0:
            easting, northing = transform_coordinates("epsg:4326", "epsg:29902", place["longitude"], place["latitude"])
            if merged.contains(Point(easting, northing)):
                places_list.append(tuple((place["population"], place["name"], place["latitude"], place["longitude"])))

    #
    # Print results
    #
    print("The address of the centroid is\n{}".format(centroid_address))
    print("\n\nPlaces by population\n")
    for place in sorted(places_list, reverse=True):
        print("{}, {}".format(place[1], place[0]))


if __name__ == "__main__":
    main()
