import sqlite3 as sql
import json
import geopandas as gpd

def get_feature_by_postcode(db_path="postcodes_multi.db", postcode_name="CM21"):
    postcode_name = postcode_name.strip().upper()
    sql_query = """SELECT data FROM postcodeDistrictGeoJSON WHERE name = ?"""

    try:
        with sql.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, (postcode_name,))
            return cursor.fetchone()
    except sql.OperationalError as e:
        print("Failed to open database: ", e)

    return None


def verify_every_postcode(db_path="postcodes_multi.db", geojson_path="PostcodeDistrictsPolygons_multi.geojson"):
    geojsonFile = open(geojson_path)
    gdf = gpd.read_file(geojsonFile)
    sql_query = """SELECT data FROM postcodeDistrictGeoJSON WHERE name = ?"""

    try:
        with sql.connect(db_path) as conn:
            cursor = conn.cursor()
            for idx, row in gdf.iterrows():
                name = row.get("name")
                cursor = conn.cursor()
                cursor.execute(sql_query, (name,))
                if not cursor.fetchone():
                    return False
    except sql.OperationalError as e:
        print("Failed to open database: ", e)
    
    return True


selectedRow = get_feature_by_postcode()
if selectedRow:
    geojson = json.loads(selectedRow[0])
    print(json.dumps(geojson, indent=4))
else:
    print("No data returned.")

if verify_every_postcode():
    print("*** EVERY POSTCODE IS PRESENT ***")