from huggingface_hub import hf_hub_download
import pandas as pd
import s2sphere

# 1. Manually download the raw metadata file (The CSV/Parquet)
# This file contains the coordinates for the world
print("Downloading Metadata File directly...")
filepath = hf_hub_download(
    repo_id="osv5m/osv5m", 
    filename="train.csv", # This is the main metadata list
    repo_type="dataset"
)

# 2. Load the file (We only load Lat/Lon to save your 18GB RAM)
print("Filtering for Bangalore...")
# Note: OSV-5M might use 'lat'/'lon' or 'latitude'/'longitude'
df = pd.read_csv(filepath, usecols=['latitude', 'longitude', 'image_id'])

# 3. Bangalore Fence (Your coordinates)
lat_min, lat_max = 12.83, 13.14
lon_min, lon_max = 77.39, 77.78

# 4. Filter the 'Shopping List'
blr_df = df[
    (df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
    (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)
].copy()

# 5. Add your Level 17 Labels (The work from Week 1)
def to_l17(row):
    ll = s2sphere.LatLng.from_degrees(row['latitude'], row['longitude'])
    return s2sphere.CellId.from_lat_lng(ll).parent(17).to_token()

print("Assigning Level 17 S2 Tokens...")
blr_df['s2_token'] = blr_df.apply(to_l17, axis=1)

# 6. Save result
blr_df.to_csv("bangalore_metadata.csv", index=False)
print(f"Success! Found {len(blr_df)} images in Bangalore.")
print("Saved to bangalore_metadata.csv")