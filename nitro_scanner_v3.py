import asyncio
import aiohttp
import pandas as pd
import os
import time
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
MAPILLARY_TOKEN ="MLY|25929808639936807|de21f268cc37e726781b9b96d0f164c6"
INPUT_GRID = "blr_grid_points.csv"
OUTPUT_FILE = "blr_mapillary_results.csv"

# Optimized for M3 Pro 18GB RAM
CONCURRENT_LIMIT = 150  # Number of simultaneous API pings
BATCH_SIZE = 2000       # How often to print progress

async def check_point(session, semaphore, index, lat, lon):
    async with semaphore:
        # The Success Formula: [min_lon, min_lat, max_lon, max_lat]
        bbox = f"{lon-0.0005},{lat-0.0005},{lon+0.0005},{lat+0.0005}"
        
        url = "https://graph.mapillary.com/images"
        params = {
            "access_token": MAPILLARY_TOKEN,
            "fields": "id",
            "bbox": bbox,
            "limit": 1
        }

        try:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {'index': index, 'mapillary': len(data.get('data', [])) > 0}
                elif resp.status == 429:
                    # Rate limit hit - return False but could implement retry
                    return {'index': index, 'mapillary': False}
        except:
            pass
        return {'index': index, 'mapillary': False}

async def main():
    if not os.path.exists(INPUT_GRID):
        print(f"Error: {INPUT_GRID} not found.")
        return

    df = pd.read_csv(INPUT_GRID)
    total = len(df)
    points = [(i, row['latitude'], row['longitude']) for i, row in df.iterrows()]
    
    results = [None] * total
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
    
    print(f"🚀 Starting Nitro Scan V3 | Points: {total} | Limit: {CONCURRENT_LIMIT}")
    start_time = time.time()

    # Use a persistent session for connection pooling
    async with aiohttp.ClientSession() as session:
        for i in range(0, total, BATCH_SIZE):
            batch = points[i:i+BATCH_SIZE]
            tasks = [check_point(session, semaphore, idx, lat, lon) for idx, lat, lon in batch]
            
            batch_results = await asyncio.gather(*tasks)
            for r in batch_results:
                results[r['index']] = r
            
            # Metrics
            done = i + len(batch)
            elapsed = time.time() - start_time
            speed = done / elapsed
            remaining = (total - done) / speed / 60
            print(f"✅ {done}/{total} | Speed: {speed:.1f} pts/sec | {remaining:.1f}m left")

    # Final Save
    df['mapillary'] = [r['mapillary'] for r in results]
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n🏁 SCAN COMPLETE!")
    print(f"Total Time: {elapsed/60:.2f} minutes")
    print(f"Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())