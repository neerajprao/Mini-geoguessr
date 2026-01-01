import pandas as pd

# Load the NEW New York metadata
try:
    df = pd.read_csv("bangalore_metadata.csv")
    unique_cells = df['s2_token'].nunique()
    avg_images = len(df) / unique_cells

    print(f"Total Images in blr: {len(df)}")
    print(f"Number of Level 15 'Boxes' (Classes): {unique_cells}")
    print(f"Average Images per Box: {avg_images:.2f}")
except FileNotFoundError:
    print("Error: nyc_metadata.csv not found. Run metadata.py first!")