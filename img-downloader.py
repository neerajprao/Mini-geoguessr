import os
import time
import io
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from PIL import Image

# --- SETTINGS ---
CSV_FILE = "monaco_roads_level16.csv"
OUTPUT_FOLDER = "Monaco_Dataset_WebP"
# ----------------

def init_stealth_driver():
    options = Options()
    # Headless can be detected; keeping it visible for higher success in Monaco
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def capture_one_location():
    # 1. Load the CSV and handle the 'Status' column
    df = pd.read_csv(CSV_FILE)
    if 'Status' not in df.columns:
        df['Status'] = ""

    # 2. Find the first row where Status is NOT "Done"
    pending_rows = df[df['Status'] != 'Done']
    
    if pending_rows.empty:
        print("All locations in Monaco are already completed!")
        return

    # Take the index of the first pending row
    idx = pending_rows.index[0]
    lat = df.at[idx, 'latitude']
    lon = df.at[idx, 'longitude']
    
    print(f"Processing row {idx}: Lat {lat}, Lon {lon}")

    # 3. Start Browser
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
    driver = init_stealth_driver()

    try:
        for i in range(8):
            heading = i * 45
            url = f"https://www.google.com/maps/@{lat},{lon},3a,75y,{heading}h,90t/data=!3m6!1e1!3m4!1s!2e0!7i16384!8i8192"
            
            driver.get(url)
            time.sleep(5) # Wait for high-res Monaco textures to load

            # Hide UI elements
            driver.execute_script("""
                document.querySelectorAll('.gmnoprint, .watermark, #pane, .scene-footer').forEach(el => el.style.display='none');
            """)
            
            # Save as WebP in RAM
            png_data = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(png_data))
            
            filename = os.path.join(OUTPUT_FOLDER, f"monaco_{lat}_{lon}_h{heading}.webp")
            img.save(filename, "WEBP", quality=80, method=6)
            print(f"Captured angle {heading}°")

        # 4. Update CSV Status
        df.at[idx, 'Status'] = 'Done'
        df.to_csv(CSV_FILE, index=False)
        print(f"Success! Saved row {idx} to CSV.")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_one_location()