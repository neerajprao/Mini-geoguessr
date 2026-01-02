import folium
from folium.plugins import FastMarkerCluster
import pandas as pd

def visualize_gaps_fast():
    df = pd.read_csv("blr_coverage_results.csv")
    
    # Filter for Gaps (Where both are False)
    gaps = df[(df['mapillary'] == False) & (df['kartaview'] == False)]
    print(f"Found {len(gaps)} gaps out of {len(df)} points.")

    # Center on Bangalore
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=11, tiles="CartoDB dark_matter")

    # Add Gaps as a FastMarkerCluster (much better for 200k+ points)
    gap_data = gaps[['latitude', 'longitude']].values.tolist()
    
    # Only visualize a sample of 50,000 for the initial map load to save RAM
    sample_size = min(50000, len(gap_data))
    FastMarkerCluster(gap_data[:sample_size]).add_to(m)

    m.save("blr_gap_map.html")
    print("Gap map saved to blr_gap_map.html.")

if __name__ == "__main__":
    visualize_gaps_fast()