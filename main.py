import requests
from bs4 import BeautifulSoup
import re  # Import regex module for cleaning price strings


def scrape_price(urls):
  prices = []
  try:
    for url_data in urls:
      url = url_data[0]
      tag_name = url_data[1]
      attributes = url_data[2]
      # Send an HTTP request to the URL
      response = requests.get(url)
      response.raise_for_status()  # Check if the request was successful

      # Parse the HTML content of the page
      soup = BeautifulSoup(response.text, 'html.parser')

      # Find the HTML element that contains the price
      price_element = soup.find(tag_name, attributes)  # Price element with id="tprice"

      if price_element:
        # Extract the price text and clean it to remove non-numerical characters
        price_text = price_element.get_text(strip=True)
        price_numeric = float(re.sub(r'[^\d.,]', '', price_text).replace(',', '.'))  # Convert to float
        prices.append(price_numeric)
      else:
        return "Price could not be found."
  except requests.exceptions.RequestException as e:
    return f"Error with the HTTP request: {e}"
  except Exception as e:
    return f"An error occurred: {e}"

  # Sort the prices in ascending order
  prices.sort()
  return prices


urls_x9 = [['https://www.gigasport.at/atomic-pistenski-set-redster-x9s-revoshock-s-x-12-gw-tuerkis-7582846.html',
            'span',
            {'id': 'tprice'}],
           ['https://www.sport-robl.at/de/ski-sets/atomic/atomic-redster-x9s-revoshock-s-laengenwahl-atomic-x-12-gw-mod-2023-2024.html',
            'span',
            {'itemprop': 'price'}]]

# Fetch prices
prices = scrape_price(urls_x9)

if isinstance(prices, list):
  print('Atomic X9 prices:')
  for price in prices:
    print(f"€ {price:.2f}")
else:
  print(prices)
