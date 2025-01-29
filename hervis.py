import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size for headless mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation features
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")  # Randomize user agent

# Use undetected-chromedriver to handle bot protection
driver = uc.Chrome(options=chrome_options)

# URL of the ski product page
url = "https://www.hervis.at/shop/Ausr%C3%BCstung/Ski/Ski-Alpin/Carvingski-Erwachsene/Atomic/REDSTER-X9S-REVOSHOCK-S-%2B-X-12-GW/p/COLOR-3298152"

# Start measuring the time for loading
start_time = time.time()

# Open the page
driver.get(url)

# Wait for the price elements to appear
try:
    # Wait until the price elements are present
    price_element = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-price__price-text"))
    )

    # Fetch the euro part of the price (main part)
    euros = price_element.text.strip()

    # Fetch the cents part of the price (decimal part)
    cents_element = driver.find_element(By.CLASS_NAME, "product-price__price-decimal")
    cents = cents_element.text.strip()

    # Full price in format 'euros.cents'
    full_price = f"{euros}.{cents}"

    # Calculate the time taken to load the page
    load_time = time.time() - start_time

    print("Price of the ski:", full_price)
    print(f"Page loaded in {load_time:.2f} seconds")

except Exception as e:
    print("Error:", e)

# Close the driver
driver.quit()
