import pandas as pd
import s2sphere
from huggingface_hub import hf_hub_download

# 1. Locate global file
filepath = hf_hub_download(repo_id="osv5m/osv5m", filename="train.csv", repo_type="dataset")

# 2. Detect Columns
sample = pd.read_csv(filepath, nrows=0)
cols = sample.columns.tolist()
lat_col = next((c for c in cols if 'lat' in c.lower()), 'latitude')
lon_col = next((c for c in cols if 'lon' in c.lower()), 'longitude')
id_col = next((c for c in cols if any(x in c.lower() for x in ['id', 'key'])), cols[0])

# 3. Manhattan "Precision Fence"
m_lat_min, m_lat_max = 40.7000, 40.8800
m_lon_min, m_lon_max = -74.0200, -73.9000

# 4. Filter in Chunks (Memory-safe for 18GB RAM)
print("Filtering Manhattan and generating L12-L17 labels...")
chunks = []
for chunk in pd.read_csv(filepath, usecols=[id_col, lat_col, lon_col], chunksize=200000):
    filtered = chunk[
        (chunk[lat_col] >= m_lat_min) & (chunk[lat_col] <= m_lat_max) &
        (chunk[lon_col] >= m_lon_min) & (chunk[lon_col] <= m_lon_max)
    ].copy()
    chunks.append(filtered)

df = pd.concat(chunks)

# 5. Generate All Levels (L12 to L17)
print(f"Processing {len(df)} images...")
for level in range(12, 18):
    col_name = f'L{level}'
    df[col_name] = df.apply(lambda r: s2sphere.CellId.from_lat_lng(
        s2sphere.LatLng.from_degrees(r[lat_col], r[lon_col])).parent(level).to_token(), axis=1)

df.to_csv("manhattan_full_levels.csv", index=False)
print("Saved to 'manhattan_full_levels.csv'")