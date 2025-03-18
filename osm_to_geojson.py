import json
import os

# Define file paths
json_file = os.path.join("Downloads", "export.json")
output_geojson = os.path.join("Downloads", "buildings.geojson")

# Load the JSON file
try:
    with open(json_file, "r", encoding="utf-8") as file:
        osm_data = json.load(file)
except FileNotFoundError:
    print(f"❌ Error: File {json_file} not found. Download your data from Overpass Turbo.")
    exit()

# Debug: Print first few elements to verify data
if "elements" not in osm_data or len(osm_data["elements"]) == 0:
    print("❌ Error: No elements found in JSON. Review your Overpass Turbo query.")
    exit()

# Extract buildings from OSM data
buildings = []
for element in osm_data["elements"]:
    if element["type"] == "way" and "building" in element.get("tags", {}):
        coords = []
        
        # Fetch nodes for the way
        for node_id in element["nodes"]:
            # Find the corresponding node data
            node_data = next((n for n in osm_data["elements"] if n["type"] == "node" and n["id"] == node_id), None)
            if node_data:
                coords.append([node_data["lon"], node_data["lat"]])

        # Ensure the polygon is closed (first == last)
        if len(coords) >= 3:
            coords.append(coords[0])
            buildings.append({"id": element["id"], "coords": coords})

# Print debug info
if len(buildings) == 0:
    print("❌ No buildings found! Check if your Overpass query is correct.")
else:
    print(f"✅ Total buildings found: {len(buildings)}")

# Convert to GeoJSON format
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"id": b["id"]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [b["coords"]],
            },
        }
        for b in buildings
    ],
}

# Save to GeoJSON file
with open(output_geojson, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)

print(f"✅ Saved to {output_geojson}")

