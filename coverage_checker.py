import asyncio
import aiohttp
import pandas as pd
import time
import os

# --- CONFIG ---
MAPILLARY_TOKEN = "YOUR_MAPILLARY_API_KEY"
INPUT_GRID = "blr_grid_points.csv"
CONCURRENT_REQUESTS = 100  # Extreme parallelization
BATCH_SIZE = 1000          # Save progress every 1k points

async def check_point(session, index, lat, lon):
    res = {'index': index, 'mapillary': False, 'kartaview': False}
    
    # 1. Mapillary Metadata (Async)
    m_url = f"https://graph.mapillary.com/images"
    m_params = {
        "access_token": MAPILLARY_TOKEN,
        "fields": "id",
        "bbox": f"{lon-0.0002},{lat-0.0002},{lon+0.0002},{lat+0.0002}",
        "limit": 1
    }
    
    # 2. KartaView Metadata (Async)
    k_url = f"https://api.kartaview.org/2.0/photos"
    k_params = {"lat": lat, "lng": lon, "radius": 40, "limit": 1}

    try:
        async with session.get(m_url, params=m_params, timeout=5) as resp:
            data = await resp.json()
            if 'data' in data and len(data['data']) > 0:
                res['mapillary'] = True
                
        async with session.get(k_url, params=k_params, timeout=5) as resp:
            data = await resp.json()
            if data.get('status', {}).get('apiCode') == '200' and data.get('data'):
                res['kartaview'] = True
    except:
        pass
    return res

async def main():
    df = pd.read_csv(INPUT_GRID)
    total = len(df)
    points = [(i, row['latitude'], row['longitude']) for i, row in df.iterrows()]
    
    results = [None] * total
    connector = aiohttp.TCPConnector(limit_per_host=CONCURRENT_REQUESTS)
    
    print(f"🚀 Launching Nitro Scan: {total} points | {CONCURRENT_REQUESTS} parallel streams")
    start_time = time.time()

    async with aiohttp.ClientSession(connector=connector) as session:
        # Process in chunks to manage memory and provide updates
        for i in range(0, total, BATCH_SIZE):
            batch = points[i:i+BATCH_SIZE]
            tasks = [check_point(session, idx, lat, lon) for idx, lat, lon in batch]
            
            batch_results = await asyncio.gather(*tasks)
            for r in batch_results:
                results[r['index']] = r
            
            # Speed Metrics
            done = i + len(batch)
            elapsed = time.time() - start_time
            speed = done / elapsed
            remaining_mins = (total - done) / speed / 60
            print(f"✅ {done}/{total} | Speed: {speed:.1f} pts/sec | Remaining: {remaining_mins:.1f}m")

    # Save Final Data
    df['mapillary'] = [r['mapillary'] for r in results]
    df['kartaview'] = [r['kartaview'] for r in results]
    df.to_csv("blr_coverage_final.csv", index=False)
    print(f"🏁 FINISHED. Total Time: {elapsed/60:.2f} mins")

if __name__ == "__main__":
    asyncio.run(main())