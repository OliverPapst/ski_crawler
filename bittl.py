from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver (ChromeDriver required)
driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
driver.get('https://www.sport-bittl.com/de/atomic-redster-x9s-revoshock-s-24-25-ski-inkl-bindung::224138.html')

# Wait for the price element to be visible (explicit wait)
try:
    # Wait until the price element is present and visible in the DOM
    price_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'fl-price-current'))
    )
    price_text = price_element.text.strip()  # Get the price text and remove extra spaces
    print(f"Price: {price_text}")
finally:
    # Close the browser
    driver.quit()
