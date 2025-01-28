import requests
from bs4 import BeautifulSoup
import re  # Import regex module for cleaning price strings
import json


def scrape_price(urls):
  prices = []
  try:
    for url_data in urls:
      shop_name = url_data[0]  # Name of the shop
      url = url_data[1]  # Product URL
      tag_name = url_data[2]  # HTML tag
      attributes = url_data[3]  # Tag attributes

      # Send an HTTP request to the URL
      response = requests.get(url)
      response.raise_for_status()  # Check if the request was successful

      # Parse the HTML content of the page
      soup = BeautifulSoup(response.text, 'html.parser')
      price_element = soup.find(tag_name, attributes)

      if price_element:
        # Find the HTML element that contains the price
        if tag_name == 'script':
          # Parse the JSON data inside the script tag
          json_data = json.loads(price_element.string)
          # Access the price within the JSON structure
          price_numeric = float(json_data['offers']['price'])
        else:
          price_text = price_element.get_text(strip=True)
          price_numeric = float(re.sub(r'[^\d.,]', '', price_text).replace(',', '.'))  # Convert to float

        # Append the shop name and price as a tuple
        prices.append((shop_name, price_numeric))
      else:
        return "Price could not be found."
  except requests.exceptions.RequestException as e:
    return f"Error with the HTTP request: {e}"
  except Exception as e:
    return f"An error occurred: {e}"

  # Sort the prices in ascending order by price (2nd element in the tuple)
  prices.sort(key=lambda x: x[1])
  return prices


# Updated input list with shop names
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
   'span',
   {'class': 'price_ausgabe'}]
]

# Fetch prices
prices = scrape_price(urls_x9)

if isinstance(prices, list):
  # Calculate the maximum length of shop names for padding
  max_shop_name_length = max(len(shop) for shop, _ in prices)

  print('##### Atomic X9 #####')
  for shop, price in prices:
    # Format output with dynamic padding based on shop name length
    print(f"{shop:<{max_shop_name_length}}: € {price:.2f}")
else:
  print(prices)
