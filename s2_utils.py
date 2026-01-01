import s2sphere

def get_s2_token_l17(lat, lon):
    """
    Converts Lat/Lon to a Level 17 Hex Token.
    Precision: ~70 meters.
    """
    # 1. Create LatLng object
    ll = s2sphere.LatLng.from_degrees(lat, lon)
    
    # 2. Map to Cell ID and truncate to Level 17
    cell_id = s2sphere.CellId.from_lat_lng(ll).parent(17)
    
    # 3. Return the Hex Token (The 'Label')
    return cell_id.to_token()

def get_metadata(token):
    """Returns center coordinates for a given token."""
    cell_id = s2sphere.CellId.from_token(token)
    latlng = cell_id.to_lat_lng()
    return latlng.lat().degrees, latlng.lng().degrees

# --- TEST RUN ---
if __name__ == "__main__":
    # Tumakuru coordinates
    t_lat, t_lon = 13.3379, 77.1173
    
    l17_token = get_s2_token_l17(t_lat, t_lon)
    c_lat, c_lon = get_metadata(l17_token)
    
    print(f"--- S2 Level 17 Results ---")
    print(f"Target Location: {t_lat}, {t_lon}")
    print(f"Level 17 Token:  {l17_token}")
    print(f"Cell Center:     {c_lat}, {c_lon}")