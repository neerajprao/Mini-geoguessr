import requests
import os
from dotenv import load_dotenv

load_dotenv()
token ="MLY|25929808639936807|de21f268cc37e726781b9b96d0f164c6".strip()

# MG Road, Bangalore
lat, lon = 12.9755, 77.6067 

# THE FIX: Mapillary BBox Order: [min_lon, min_lat, max_lon, max_lat]
# We use a 0.001 offset (~110 meters) to ensure we hit the road
min_lon = lon - 0.001
min_lat = lat - 0.001
max_lon = lon + 0.001
max_lat = lat + 0.001

bbox = f"{min_lon},{min_lat},{max_lon},{max_lat}"
url = f"https://graph.mapillary.com/images?access_token={token}&fields=id&bbox={bbox}&limit=1"

print(f"--- Hard-Fix Diagnostic (Attempt 3) ---")
print(f"Searching BBox: {bbox}")

try:
    res = requests.get(url, timeout=10)
    data = res.json()
    print(f"Status: {res.status_code}")
    print(f"Data Found: {data}")
    if res.status_code == 200 and len(data.get('data', [])) > 0:
        print("✅ SUCCESS! The coordinate order is now correct.")
except Exception as e:
    print(f"Error: {e}")