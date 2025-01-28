import requests
from bs4 import BeautifulSoup

def scrape_price(url):
    try:
        # Sende eine HTTP-Anfrage an die URL
        response = requests.get(url)
        response.raise_for_status()  # Überprüfe, ob die Anfrage erfolgreich war

        # Parse den HTML-Inhalt der Seite
        soup = BeautifulSoup(response.text, 'html.parser')

        # Schön lesbar den Soup ausgeben
        # print(soup.prettify())

        # Suche das HTML-Element, das den Preis enthält
        price_element = soup.find('span', id='tprice')  # Preis-Element mit id="tprice"

        if price_element:
            # Extrahiere den Preis-Text
            price = price_element.get_text(strip=True)
            return price
        else:
            return "Preis konnte nicht gefunden werden."
    except requests.exceptions.RequestException as e:
        return f"Fehler bei der HTTP-Anfrage: {e}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"


# URL des Produkts
url = "https://www.gigasport.at/atomic-pistenski-set-redster-x9s-revoshock-s-x-12-gw-tuerkis-7582846.html"

# Preis abrufen
price = scrape_price(url)
print(f"Der Preis des Produkts ist: {price}")
