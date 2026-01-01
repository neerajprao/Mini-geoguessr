import s2sphere
import folium

def draw_l17_map(lat, lon, filename="level17_map.html"):
    # 1. Get the Token and the Cell object
    ll = s2sphere.LatLng.from_degrees(lat, lon)
    cell_id = s2sphere.CellId.from_lat_lng(ll).parent(17)
    cell = s2sphere.Cell(cell_id)
    token = cell_id.to_token()

    # 2. Get the 4 corners (vertices) for the boundary
    vertices = []
    for i in range(4):
        v = s2sphere.LatLng.from_point(cell.get_vertex(i))
        vertices.append([v.lat().degrees, v.lng().degrees])

    # 3. Create the Map (Zoomed in close)
    m = folium.Map(location=[lat, lon], zoom_start=19, tiles="openstreetmap")

    # 4. Add the Level 17 Polygon
    folium.Polygon(
        locations=vertices,
        color="red",
        weight=5,
        fill=True,
        fill_color="red",
        fill_opacity=0.2,
        popup=f"Level 17 Cell: {token}"
    ).add_to(m)

    # 5. Add a marker for the exact point
    folium.Marker([lat, lon], tooltip="Input Point").add_to(m)

    m.save(filename)
    print(f"Success! Level 17 map saved as {filename}")

if __name__ == "__main__":
    # Change these to your home/uni coordinates to see the 'Box'
    draw_l17_map(13.3379, 77.1173)