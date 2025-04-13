import geopandas as gpd
import sqlite3 as sql
import json

def create_geojson_db(gdf, dbpath = "postcodes.db"):
    sql_create = """CREATE TABLE IF NOT EXISTS postcodeDistrictGeoJSON (
        name TEXT PRIMARY KEY,
        data TEXT UNIQUE NOT NULL
    );"""

    sql_insert = """INSERT INTO postcodeDistrictGeoJSON(name, data) VALUES(?, ?);"""

    try:
        with sql.connect(dbpath) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_create)
            conn.commit()
            print("*** Talbe created ***")

            # Iterate the features in the geopandas df
            for idx, row in gdf.iterrows():
                name = row.get("name")
                print(name)
                geometry_json = row.geometry.__geo_interface__
                
                # Construct the name and geometry into a geojson feature 
                feature = {
                    'type': 'Feature',
                    "geometry": geometry_json,
                    "properties": {
                        "name": name
                    }
                }
                # Place the geojson feature within a feature collection
                # This allows the feature to be read-in by maps as a complete geojson object/file
                collection = {
                    'type': 'FeatureCollection',
                    'features': [
                        feature
                    ]
                }
                featureString = json.dumps(collection)
                cursor.execute(sql_insert, (name, featureString))
            conn.commit()
    except sql.OperationalError as e:
        print("Failed to open database:", e)


# Load geojson
path = "PostcodeDistrictsPolygons_multi.geojson"
file = open(path)
df = gpd.read_file(file)

create_geojson_db(df, "postcodes_multi.db")