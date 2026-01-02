import requests
import os
from dotenv import load_dotenv

load_dotenv()
token ="MLY|25929808639936807|de21f268cc37e726781b9b96d0f164c6".strip()

# A guaranteed spot: Near Cubbon Park/MG Road
lat, lon = 12.9755, 77.6067 

print(f"--- Hard-Fix Diagnostic ---")

# 1. Mapillary Point Search (Alternative to BBox)
# Mapillary v4 uses a very specific bbox: [min_lon, min_lat, max_lon, max_lat]
bbox = f"{lon-0.005},{lat-0.005},{lon+0.005},{lat+0.005}"
url = f"https://graph.mapillary.com/images?access_token={token}&fields=id,geometry&bbox={bbox}&limit=1"

try:
    res = requests.get(url, timeout=10)
    print(f"Mapillary Status: {res.status_code}")
    print(f"Mapillary Raw Body: {res.text}")
except Exception as e:
    print(f"Mapillary Error: {e}")

# 2. KartaView Public Search
k_url = f"https://api.kartaview.org/2.0/photos?lat={lat}&lng={lon}&radius=500&limit=1"
try:
    k_res = requests.get(k_url, timeout=10)
    print(f"\nKartaView Status: {k_res.status_code}")
    print(f"KartaView Data Found: {bool(k_res.json().get('data'))}")
except Exception as e:
    print(f"KartaView DNS/Network Error: {e}")