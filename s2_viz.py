import s2sphere
import folium

def get_cell_vertices(lat, lon, level):
    """Calculates the 4 corner coordinates for a given level."""
    ll = s2sphere.LatLng.from_degrees(lat, lon)
    cell_id = s2sphere.CellId.from_lat_lng(ll).parent(level)
    cell = s2sphere.Cell(cell_id)
    vertices = []
    for i in range(4):
        v = s2sphere.LatLng.from_point(cell.get_vertex(i))
        vertices.append([v.lat().degrees, v.lng().degrees])
    return vertices, cell_id.to_token()

# Coordinates from your Task A run
target_lat, target_lon = 13.3379, 77.1173

# Initialize map
m = folium.Map(location=[target_lat, target_lon], zoom_start=18, tiles="openstreetmap")

# --- LEVEL 15 (Blue) ---
coords_15, token_15 = get_cell_vertices(target_lat, target_lon, 15)
folium.Polygon(
    locations=coords_15,
    color="blue", weight=2, fill=True, fill_opacity=0.1,
    popup=f"Level 15: {token_15} (~300m)"
).add_to(m)

# --- LEVEL 17 (Red) ---
coords_17, token_17 = get_cell_vertices(target_lat, target_lon, 17)
folium.Polygon(
    locations=coords_17,
    color="red", weight=4, fill=True, fill_opacity=0.3,
    popup=f"Level 17: {token_17} (~75m)"
).add_to(m)

# Marker for your target point
folium.Marker([target_lat, target_lon], tooltip="Your Target").add_to(m)

m.save("s2_comparison.html")
print("Visualized! Open 's2_comparison.html' in your browser.")