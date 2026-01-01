import folium
from folium import LayerControl
import pandas as pd
import s2sphere

def visualize_manhattan_all_levels(csv_path):
    df = pd.read_csv(csv_path)
    
    # Initialize map centered on Manhattan
    m = folium.Map(location=[40.7831, -73.9712], zoom_start=13, tiles="CartoDB positron")
    
    # Colors for different levels
    colors = {
        'L12': 'blue',   # City Sector
        'L13': 'green',  # Neighborhood
        'L14': 'orange', # 4-6 Blocks
        'L15': 'red',    # 1-2 Blocks
        'L16': 'purple', # Alleyway
        'L17': 'black'   # Building plot
    }

    # Create a FeatureGroup for each level
    for level in range(12, 18):
        col_name = f'L{level}'
        group = folium.FeatureGroup(name=f"Level {level} ({colors[col_name]})")
        
        # Get unique tokens for this level to avoid over-drawing
        unique_tokens = df[col_name].unique()
        print(f"Adding {len(unique_tokens)} tiles for Level {level}...")

        # Limit to first 100 tiles for higher levels to keep the file size usable
        limit = 100 if level > 14 else len(unique_tokens)
        
        for token in unique_tokens[:limit]:
            cell_id = s2sphere.CellId.from_token(token)
            cell = s2sphere.Cell(cell_id)
            
            vertices = []
            for i in range(4):
                v = s2sphere.LatLng.from_point(cell.get_vertex(i))
                vertices.append([v.lat().degrees, v.lng().degrees])
            
            folium.Polygon(
                locations=vertices,
                color=colors[col_name],
                weight=2,
                fill=True,
                fill_opacity=0.1,
                popup=f"Level {level} Token: {token}"
            ).add_to(group)
        
        group.add_to(m)

    # Add toggle control
    LayerControl().add_to(m)
    
    out_file = "manhattan_full_viz.html"
    m.save(out_file)
    print(f"Success! Open '{out_file}' to see the Manhattan S2 grid.")

if __name__ == "__main__":
    visualize_manhattan_all_levels("manhattan_full_levels.csv")