import pandas as pd

# Load the London L15 metadata
try:
    df = pd.read_csv("london_l15_metadata.csv")
    unique_cells = df['s2_token'].nunique()
    avg_images = len(df) / unique_cells

    print(f"\n--- London Level 15 Diagnostic ---")
    print(f"Total Images: {len(df)}")
    print(f"Number of Level 15 Boxes (Classes): {unique_cells}")
    print(f"Average Images per Box: {avg_images:.2f}")
    
    # Check for the 'Top' cells to see the density
    print("\nTop 5 densest cells:")
    print(df['s2_token'].value_counts().head(5))

except FileNotFoundError:
    print("Error: london_l15_metadata.csv not found.")