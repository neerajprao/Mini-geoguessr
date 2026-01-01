import folium
import pandas as pd
import s2sphere
import os

def visualize_bangalore(csv_path, level=13):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        return

    df = pd.read_csv(csv_path)
    print(f"Read {len(df)} rows from CSV.")

    # Calculate tokens for the requested level
    def get_token(row):
        ll = s2sphere.LatLng.from_degrees(row['latitude'], row['longitude'])
        return s2sphere.CellId.from_lat_lng(ll).parent(level).to_token()

    df['viz_token'] = df.apply(get_token, axis=1)
    unique_tokens = df['viz_token'].unique()
    print(f"Found {len(unique_tokens)} unique Level {level} boxes to draw.")

    # Center map on the average of your data points
    avg_lat = df['latitude'].mean()
    avg_lon = df['longitude'].mean()
    print(f"Centering map at: {avg_lat}, {avg_lon}")
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    for token in unique_tokens[:500]: # Limit to 500 for speed
        cell_id = s2sphere.CellId.from_token(token)
        cell = s2sphere.Cell(cell_id)
        
        vertices = []
        for i in range(4):
            v = s2sphere.LatLng.from_point(cell.get_vertex(i))
            vertices.append([v.lat().degrees, v.lng().degrees])
        
        folium.Polygon(
            locations=vertices,
            color="blue" if level == 12 else "red",
            fill=True,
            fill_opacity=0.3,
            popup=f"L{level} Token: {token}"
        ).add_to(m)

    out_file = f"blr_l{level}_viz.html"
    m.save(out_file)
    print(f"SUCCESS: Map saved as {out_file} in your current folder.")

# Run for both levels
visualize_bangalore('bangalore_metadata.csv', level=12)
visualize_bangalore('bangalore_metadata.csv', level=13)