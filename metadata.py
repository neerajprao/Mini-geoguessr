import pandas as pd
import s2sphere
from huggingface_hub import hf_hub_download
import os

# 1. Locate the file you already downloaded (2.92GB)
# This will return the path immediately without re-downloading
print("Locating your 2.92GB metadata file...")
filepath = hf_hub_download(
    repo_id="osv5m/osv5m", 
    filename="train.csv", 
    repo_type="dataset"
)
print(f"File found at: {filepath}")

# 2. PEEK AT HEADERS: Let's see what the columns are actually named
# This prevents the 'ValueError' from your previous run
print("Checking CSV headers...")
sample = pd.read_csv(filepath, nrows=5)
cols = sample.columns.tolist()
print(f"Available columns: {cols}")

# Find the right columns dynamically
# In OSV-5M, these are often 'latitude', 'longitude', and 'id'
lat_col = next((c for c in cols if 'lat' in c.lower()), None)
lon_col = next((c for c in cols if 'lon' in c.lower()), None)
id_col = next((c for c in cols if any(x in c.lower() for x in ['id', 'key', 'name'])), cols[0])

# 3. CHUNKED PROCESSING: Filter for Bangalore
# This keeps your 18GB RAM safe by only looking at 100k rows at a time
print(f"Filtering for Bangalore using: {id_col}, {lat_col}, {lon_col}...")
lat_min, lat_max = 12.83, 13.14
lon_min, lon_max = 77.39, 77.78

blr_chunks = []
for chunk in pd.read_csv(filepath, usecols=[id_col, lat_col, lon_col], chunksize=100000):
    filtered = chunk[
        (chunk[lat_col] >= lat_min) & (chunk[lat_col] <= lat_max) &
        (chunk[lon_col] >= lon_min) & (chunk[lon_col] <= lon_max)
    ].copy()
    blr_chunks.append(filtered)

blr_df = pd.concat(blr_chunks)

# 4. LEVEL 17 LABELING: Your project's "Fingerprint" logic
print(f"Generating Level 17 Tokens for {len(blr_df)} images...")
def to_l17(row):
    ll = s2sphere.LatLng.from_degrees(row[lat_col], row[lon_col])
    # Level 17 provides the ~70m precision for Bangalore
    return s2sphere.CellId.from_lat_lng(ll).parent(17).to_token()

blr_df['s2_token'] = blr_df.apply(to_l17, axis=1)

# 5. SAVE RESULT
blr_df.to_csv("bangalore_metadata.csv", index=False)
print(f"Success! Found {len(blr_df)} images in Bangalore.")
print("Saved to 'bangalore_metadata.csv'")