import pandas as pd
import s2sphere
from huggingface_hub import hf_hub_download

# 1. Locate the file (No re-downloading)
print("Locating global metadata...")
filepath = hf_hub_download(repo_id="osv5m/osv5m", filename="train.csv", repo_type="dataset")

# 2. Detect Columns
sample = pd.read_csv(filepath, nrows=0)
cols = sample.columns.tolist()
lat_col = next((c for c in cols if 'lat' in c.lower()), 'latitude')
lon_col = next((c for c in cols if 'lon' in c.lower()), 'longitude')
id_col = next((c for c in cols if any(x in c.lower() for x in ['id', 'key'])), cols[0])

# 3. London Boundary (Greater London)
lon_min, lon_max = -0.5103, 0.3340
lat_min, lat_max = 51.2867, 51.6918

# 4. Filter for London
print(f"Filtering 5M rows for London...")
ldn_chunks = []
for chunk in pd.read_csv(filepath, usecols=[id_col, lat_col, lon_col], chunksize=200000):
    filtered = chunk[
        (chunk[lat_col] >= lat_min) & (chunk[lat_col] <= lat_max) &
        (chunk[lon_col] >= lon_min) & (chunk[lon_col] <= lon_max)
    ].copy()
    ldn_chunks.append(filtered)
ldn_df = pd.concat(ldn_chunks)

# 5. Apply Level 15 Labels
print("Generating Level 15 Tokens...")
ldn_df['s2_token'] = ldn_df.apply(
    lambda r: s2sphere.CellId.from_lat_lng(
        s2sphere.LatLng.from_degrees(r[lat_col], r[lon_col])
    ).parent(15).to_token(), axis=1
)

# 6. Save
ldn_df.to_csv("london_l15_metadata.csv", index=False)
print(f"Success! London L15 dataset saved with {len(ldn_df)} images.")