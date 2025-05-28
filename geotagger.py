import json

def is_valid_coordinate(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)

def convert_to_geojson(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    skipped = 0
    for item in data:
        lat = item.get("latitude")
        lon = item.get("longitude")

        if is_valid_coordinate(lat) and is_valid_coordinate(lon):
            feature = {
                "type": "Feature",
                "properties": {
                    "name": item.get("name", ""),
                    "city": item.get("city", ""),
                    "query": item.get("query", "")
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            }
            geojson["features"].append(feature)
        else:
            skipped += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(geojson['features'])} valid items.")
    if skipped:
        print(f"⚠️ Skipped {skipped} item(s) due to invalid coordinates.")

# Usage
input_json_path = "poi.json"
output_geojson_path = "poi.geojson"

convert_to_geojson(input_json_path, output_geojson_path)
