import os
import time
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# --- CONFIGURATION ---
# Sample Bangalore coordinates (Road-only)
LOCATIONS = [
    (12.9756, 77.6067),  # MG Road
    (12.9279, 77.6271),  # Koramangala
]
OUTPUT_FOLDER = "Bangalore_Dataset_WebP"
# ---------------------

def setup_driver():
    chrome_options = Options()
    # options.add_argument("--headless") # Uncomment to run in background
    chrome_options.add_argument("--window-size=1920,1080") # High Resolution
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def capture_and_convert(driver, lat, lon, folder):
    if not os.path.exists(folder): os.makedirs(folder)

    for i in range(8):
        heading = i * 45
        # The URL structure controls the camera angle:
        # 3a (Street View), 75y (FOV), {heading}h (Rotation), 90t (Pitch)
        url = f"https://www.google.com/maps/@{lat},{lon},3a,75y,{heading}h,90t/data=!3m6!1e1!3m4!1s!2e0!7i16384!8i8192"
        
        driver.get(url)
        time.sleep(4) # Wait for high-res textures to load

        # HIDE UI ELEMENTS: CSS Injection to remove buttons, search bars, and labels
        driver.execute_script("""
            var selectors = [
                '.widget-image-header', '.scene-footer', '#pane', 
                '#titlecard', '.id-omnibox-container', '.gmnoprint',
                '.app-viewcard-strip', '.watermark'
            ];
            selectors.forEach(selector => {
                var elements = document.querySelectorAll(selector);
                elements.forEach(el => el.style.display = 'none');
            });
        """)
        
        # Take screenshot as binary data (saves disk I/O)
        png_data = driver.get_screenshot_as_png()
        
        # Convert to WebP using Pillow
        img = Image.open(io.BytesIO(png_data))
        filename = f"{folder}/blr_{lat}_{lon}_h{heading}.webp"
        
        # quality=80 is the sweet spot: high clarity, very low size
        # method=6 makes the compression much more efficient (but slightly slower)
        img.save(filename, "WEBP", quality=80, method=6)
        print(f"Saved optimized WebP: {filename}")

def main():
    driver = setup_driver()
    try:
        for lat, lon in LOCATIONS:
            print(f"Processing location: {lat}, {lon}")
            capture_and_convert(driver, lat, lon, OUTPUT_FOLDER)
    finally:
        driver.quit()
        print("Done!")

if __name__ == "__main__":
    main()