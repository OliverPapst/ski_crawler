import requests
from bs4 import BeautifulSoup
import re  # Import regex module for cleaning price strings
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

urls_x9 = [
    ['Gigasport',
     'https://www.gigasport.at/atomic-pistenski-set-redster-x9s-revoshock-s-x-12-gw-tuerkis-7582846.html',
     'span',
     {'id': 'tprice'}],
    ['Sport Robl',
     'https://www.sport-robl.at/de/ski-sets/atomic/atomic-redster-x9s-revoshock-s-laengenwahl-atomic-x-12-gw-mod-2023-2024.html',
     'span',
     {'itemprop': 'price'}],
    ['Intersport',
     'https://www.intersport.at/p/atomic-redster-x9s-revoshock-s-race-alpinski-iat.atomic.aass03266.000.html',
     'script',
     {'id': 'schema-org-pdp', 'type': 'application/ld+json'}],
    ['Sport Bittl',
     'https://www.sport-bittl.com/de/alpin-ski-vormontiert/?part=186&action=asp&pid=46-186-224138',
     'div',
     {'class': 'set-configurator-widget__infos__price--current'}],
    ['Sport Ueberbacher',
     'https://www.sport-ueberbacher.at/redster_x9s_revoshock_s_x_12_gw_2024_25-3616.htm',
     'span',
     {'class': 'price_ausgabe'}],
    ['Hervis',
     'https://www.hervis.at/shop/Ausr%C3%BCstung/Ski/Ski-Alpin/Carvingski-Erwachsene/Atomic/REDSTER-X9S-REVOSHOCK-S-%2B-X-12-GW/p/COLOR-3298152',
     '',
     {}],
    ['Bruendl Sports',
     'https://www.bruendl.at/en/products-brands/products/equipment/atomic-redster-x9-s-rvsk-s-x-12-gw',
     'script',
     {'type': 'application/ld+json'}],
    ['SportOkay',
     'https://www.sportokay.com/at_de/atomic-redster-x9s-revoshock-s-x-12-gw-skiset-2024.html',
     'meta',
     {'itemprop': 'price'}]
]
# Fetch prices X9
# prices = scrape_price(urls_x9)
# print('######## Atomic X9 ########')
# print_prices(prices)

urls_s9 = [
    ['Gigasport',
     'https://www.gigasport.at/atomic-raceski-redster-s9-rvsk-s-x-12-gw-rot-7661693.html',
     'span',
     {'id': 'tprice'}],
    ['Sport Robl S9 23/24',
     'https://www.sport-robl.at/de/ski-sets/atomic/atomic-redster-s9-revoshock-s-laengenwahl-atomic-x-12-gw-mod-2023-2024.html',
     'span',
     {'itemprop': 'price'}],
    ['Sport Robl S9 24/25',
     'https://www.sport-robl.at/de/ski-sets/atomic/atomic-redster-s9-revoshock-s-laengenwahl-atomic-x-12-gw-re-mod-2024-2025.html',
     'span',
     {'itemprop': 'price'}],
    ['Intersport',
     'https://www.intersport.at/p/atomic-redster-s9-revoshock-s-afi-race-alpinski-iat.atomic.aass03410.000.html',
     'script',
     {'id': 'schema-org-pdp', 'type': 'application/ld+json'}],
    ['Sport Bittl',
     'https://www.sport-bittl.com/de/atomic-redster-s9-revoshock-s-24-25-ski-inkl-bindung::231323.html',
     'div',
     {'class': 'set-configurator-widget__infos__price--current'}],
    # ['Sport Ueberbacher', # NO S9
    #  '',
    #  'span',
    #  {'class': 'price_ausgabe'}],
    ['Hervis',
     'https://www.hervis.at/shop/Ausr%C3%BCstung/Ski/Ski-Alpin/Carvingski-Erwachsene/Atomic/Redster-S9-Revoshock-S/p/COLOR-3391677',
     '',
     {}],
    ['Bruendl Sports',
     'https://www.bruendl.at/de/produkte-marken/produkte/ausruestung/atomic-redster-s9-revo-x-12-gw',
     'script',
     {'type': 'application/ld+json'}],
    ['SportOkay',
     'https://www.sportokay.com/at_de/atomic-redster-s9-revoshock-s-x-12-gw-skiset-2024.html',
     'meta',
     {'itemprop': 'price'}]
]

def scrape_hervis_price(url):
    """Fetch price from Hervis using Selenium (since it blocks requests)"""
    driver = uc.Chrome()
    try:
        driver.get(url)
        # Start measuring the time for loading
        start_time = time.time()
        # Wait until the price elements are present
        price_element = WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-price__price-text"))
        )
        # Fetch the euro part of the price (main part)
        euros = price_element.text.strip()
        # Fetch the cents part of the price (decimal part)
        cents_element = driver.find_element(By.CLASS_NAME, "product-price__price-decimal")
        cents = cents_element.text.strip()
        # Combine price parts
        full_price = float(f"{euros}{cents}".replace(',', '.'))
        # Calculate loading time
        load_time = time.time() - start_time
        # print(f"Price of the ski: € {full_price:.2f}")
        # print(f"Page loaded in {load_time:.2f} seconds")
        driver.quit()
        return full_price
    except Exception as e:
        driver.quit()
        return f"Error fetching Hervis price: {e}"


def scrape_price(urls):
    """Fetch prices from multiple websites using BeautifulSoup & Selenium for Hervis"""
    prices = []
    try:
        for url_data in urls:
            shop_name = url_data[0]  # Name of the shop
            url = url_data[1]  # Product URL
            tag_name = url_data[2]  # HTML tag
            attributes = url_data[3]  # Tag attributes

            # Special case for Hervis (requires Selenium)
            if shop_name.lower() == "hervis":
                price_numeric = scrape_hervis_price(url)
                if isinstance(price_numeric, float):
                    prices.append((shop_name, price_numeric))
                else:
                    print(price_numeric)  # Print error message if it failed
                continue  # Skip the rest of the loop for Hervis

            # Fetch price with requests + BeautifulSoup for other shops
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # price_element = soup.find(tag_name, attributes)
            price_element = soup.find_all(tag_name, attributes)

            if price_element:
                price_numeric = None
                if tag_name == 'script':
                    for script_tag in price_element:
                        try:
                            # Parse the JSON data from the script tag
                            json_data = json.loads(script_tag.string)
                            # Check if the JSON contains product offers and price
                            if 'offers' in json_data and 'price' in json_data['offers']:
                                price_numeric = float(json_data['offers']['price'])
                                break  # Stop once we find the price
                        except json.JSONDecodeError:
                            continue  # Skip if there is any issue with parsing the JSON
                elif tag_name == 'meta':  # Handling meta tag
                    price_numeric = float(price_element[0]['content'])
                else:
                    price_text = price_element[0].get_text(strip=True)
                    price_numeric = float(re.sub(r'[^\d.,]', '', price_text).replace(',', '.'))

                prices.append((shop_name, price_numeric))
            else:
                print(f"Price not found for {shop_name}.")
    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Sort prices in ascending order
    prices.sort(key=lambda x: x[1])
    return prices


def print_prices(prices):
    if isinstance(prices, list):
        max_shop_name_length = max(len(shop) for shop, _ in prices)
        for shop, price in prices:
            print(f"{shop:<{max_shop_name_length}}: € {price:.2f}")
    else:
        print(prices)

# Fetch prices S9
prices = scrape_price(urls_s9)
print('######## Atomic S9 ########')
print_prices(prices)

# TODO:
# decathlon - no revoshock models available
# sport 2000 - 1260€
# https://sport2000.at/de/atomic-redster-x9s-rvsk-s-+-x-12-gw/p-M0887445367062?delivery-method=10001&payment-mode=online&vendor=227