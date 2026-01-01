import s2sphere

def get_s2_token(lat, lon, level=17):
    """Converts Lat/Lon to a Level 15 Hex Token (The 'Label')"""
    ll = s2sphere.LatLng.from_degrees(lat, lon)
    cell_id = s2sphere.CellId.from_lat_lng(ll).parent(level)
    return cell_id.to_token()

def get_center_from_token(token):
    """Converts a Hex Token back to Lat/Lon (For checking accuracy)"""
    cell_id = s2sphere.CellId.from_token(token)
    latlng = cell_id.to_lat_lng()
    return latlng.lat().degrees, latlng.lng().degrees

# --- TEST CASE: Tumakuru University Area ---
test_lat, test_lon = 13.3379, 77.1173
token = get_s2_token(test_lat, test_lon)
center_lat, center_lon = get_center_from_token(token)

print(f"Target: {test_lat}, {test_lon}")
print(f"S2 Level 15 Token: {token}")
print(f"Cell Center: {center_lat}, {center_lon}")