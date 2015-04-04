"""
Make a shapefile from data in PostGIS.
"""
__author__ = 'mark'

from shapely.geometry import Point, Polygon, mapping, shape
import fiona
from fiona.crs import from_epsg
from os import path
import pyproj

OUTPUT_DIR = ".cache"
POINT_SHP = path.join(OUTPUT_DIR,"geoname_pop5000_postgis.shp")
SHP_SCHEMA = {'geometry': 'Point', 'properties': {'name': 'str', 'population': 'int'}}
DB_CONN_STRING = "dbname=census2011 user=student password=student host=83.212.126.59 port=5432"
DB_QUERY = "SELECT * FROM geonames_populated"

import psycopg2
import psycopg2.extras

def get_db_data():
    """
    Makes a connection to a PostgreSQL database and creates a cursor representing a collection of rows. The elements in
    these rows can be accessed by numeric index or column name.

    :return: List of rows representing query result set.
    """

    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(DB_QUERY)
            c = cur.fetchall()
            cur.close()
            return c
        except psycopg2.Error as e:
            print(e)
            return None

    except psycopg2.OperationalError as e:
        print(e)
        return None


def make_shapefile(db_cursor):
    """
    Makes a new shapefile names as per POINT_SHP. This is created using data from earlier PostgreSQL query.

    :param db_cursor: Data rows from query result set
    :return: None. shapefile is created in function.
    """

    with fiona.open(POINT_SHP, "w", "ESRI Shapefile", SHP_SCHEMA, crs=from_epsg(4326)) as output:
        for row in db_cursor:
            point = Point(float(row['longitude']), float(row['latitude']))
            output.write({
                'properties': {
                    'name': row['name'],
                    'population': row['population']
                },
                'geometry': mapping(point)
            })

def main():
    my_cur = get_db_data()
    if my_cur:
        make_shapefile(my_cur)


if __name__ == "__main__":
    main()