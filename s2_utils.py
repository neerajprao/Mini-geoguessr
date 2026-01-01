import os
import shutil
import pandas as pd
import s2sphere

def organize_by_s2(csv_path, image_dir, target_level=13):
    """
    Moves images into folders named after their S2 tokens.
    """
    df = pd.read_csv(csv_path)
    output_base = f"data/blr_L{target_level}"
    
    print(f"Organizing images for Level {target_level}...")
    
    for _, row in df.iterrows():
        # Get the token for the requested level
        ll = s2sphere.LatLng.from_degrees(row['latitude'], row['longitude'])
        cell_id = s2sphere.CellId.from_lat_lng(ll).parent(target_level)
        token = cell_id.to_token()
        
        # Paths
        src_path = os.path.join(image_dir, f"{row['id']}.jpg")
        dest_dir = os.path.join(output_base, token)
        
        if os.path.exists(src_path):
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy(src_path, os.path.join(dest_dir, f"{row['id']}.jpg"))
            
    print(f"Done! Data organized in {output_base}")

# Usage: 
# organize_by_s2('bangalore_metadata.csv', 'data/images', target_level=13)