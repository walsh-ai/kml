#
import geopandas as gpd
from lxml import etree
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely import to_geojson

def kml_to_geojson(kml_file):
    # Parse the kml file 
    tree = etree.parse(kml_file)
    root = tree.getroot()

    # Define KML namespaces 
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    placemarks = root.xpath('//kml:Placemark', namespaces=ns)

    features = []

    count = 0
    for placemark in placemarks:
        name = placemark.find('kml:name', namespaces=ns).text
        description = placemark.find('kml:description', namespaces=ns).text

        polygon_coords = placemark.xpath('.//kml:Polygon//kml:coordinates', namespaces=ns)

        coords_list = []
        for coord_tags in polygon_coords:
            cdtext = coord_tags.text.strip()

            # Coordinates to list of tuples
            coords = []
            for coord in cdtext.split():
                lon, lat, _ = coord.split(',')  # Ignoring the altitude
                coords.append((float(lon), float(lat)))
            coords_list.append(coords)

        # Create a geojson polygon from coordinates
        
        polygon = _
        if len(coords_list) > 1:
            polygons = [Polygon(coords) for coords in coords_list]
            polygon = MultiPolygon(polygons)
        else:
            polygon = Polygon(coords_list[0])
            # gjs_polygon = to_geojson(polygon)

        # Create a descriptive feature 
        feature = {
            'type': 'Feature',
            "geometry": polygon.__geo_interface__,
            "properties": {
                "name": name
            }
        }
        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    return geojson

kml_file = 'PostcodeDistricts.kml'
geojson = kml_to_geojson(kml_file)

num_features = len(geojson['features'])
print(f'There are {num_features} features in the GeoJSON FeatureCollection.')

write = True
# write = False
if write:
    import json
    with open('PostcodeDistrictsPolygons_multi.geojson', 'w') as f:
        json.dump(geojson, f, indent=4)

print("Conversion Complete")

# To database 
#import sqlite3
#import json
# #from sqlalchemy import create_engine

# def create_geojson_db(_geojson, db_path="postcodes.db"):
#     sql_create = """CREATE TABLE IF NOT EXISTS postcodeDistrictGeoJSON (
#         name TEXT PRIMARY KEY,
#         data TEXT UNIQUE NOT NULL
#     );"""

#     sql_insert = """INSERT INTO postcodeDistrictGeoJSON(name, data) VALUES(?, ?)"""

#     try:
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute(sql_create)
#             conn.commit()
#             print("Table created.")

#             for feature in _geojson['features']:
#                 newName = feature['properties']['name']
#                 print(newName)
#                 featureString = json.dumps(feature)
#                 cursor.execute(sql_insert, (newName, featureString))
#             conn.commit()
#     except sqlite3.OperationalError as e:
#         print("Failed to open database:", e)


# create_geojson_db(geojson)