import pandas as pd

df = pd.read_csv("manhattan_full_levels.csv")
total_imgs = len(df)

results = []
for level in range(12, 18):
    col = f'L{level}'
    unique_cells = df[col].nunique()
    avg = total_imgs / unique_cells
    results.append({"Level": level, "Unique Classes": unique_cells, "Avg Images/Box": round(avg, 2)})

report = pd.DataFrame(results)
print("\n--- MANHATTAN DENSITY REPORT ---")
print(report.to_string(index=False))