import osmnx as ox
import mercantile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def get_monaco_roads_by_tiles(zoom_level=16):
    print(f"Fetching road network for Monaco...")
    
    # 1. Fetch road network for Monaco
    # Monaco is small, so 'network_type='all'' will capture every street and walkway
    try:
        graph = ox.graph_from_place("Monaco", network_type='all')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
    # Convert graph to GeoDataFrame (edges represent the roads)
    nodes, edges = ox.graph_to_gdfs(graph)
    
    # 2. Get the bounding box of the country
    west, south, east, north = edges.total_bounds
    
    # 3. Generate all tiles at the specified zoom level
    tiles = list(mercantile.tiles(west, south, east, north, zoom_level))
    print(f"Total tiles to process at Level {zoom_level}: {len(tiles)}")
    
    tile_data = []

    # 4. Extract road coordinates and map them to tiles
    for _, row in edges.iterrows():
        # Handle different geometry types
        if row.geometry.geom_type == 'LineString':
            coords = list(row.geometry.coords)
        elif row.geometry.geom_type == 'MultiLineString':
            coords = [c for line in row.geometry.geoms for c in line.coords]
        else:
            continue

        for lon, lat in coords:
            # Map coordinate to Slippy Map tile
            tile = mercantile.tile(lon, lat, zoom_level)
            tile_data.append({
                'latitude': lat,
                'longitude': lon,
                'tile_x': tile.x,
                'tile_y': tile.y,
                'tile_z': tile.z,
                'road_name': row.get('name', 'Unnamed Road')
            })

    # 5. Clean and Save
    df = pd.DataFrame(tile_data)
    df = df.drop_duplicates(subset=['latitude', 'longitude', 'tile_x', 'tile_y'])
    
    output_file = f"monaco_roads_level{zoom_level}.csv"
    df.to_csv(output_file, index=False)
    
    print(f"Success! Found {len(df)} unique road points across {len(tiles)} tiles.")
    print(f"Data saved to {output_file}")
    return df

if __name__ == "__main__":
    get_monaco_roads_by_tiles(zoom_level=16)