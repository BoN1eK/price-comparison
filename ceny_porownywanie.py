import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Funkcja do zbierania danych
def get_product_prices(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # Pobieranie zawartości strony
    page = requests.get(url, headers=headers)

    # Parsowanie HTML
    soup = BeautifulSoup(page.content, 'html.parser')

    # Listy do przechowywania produktów i cen
    products = []
    prices = []

    # Znalezienie produktów i cen na stronie Nike
    for product in soup.findAll('div', {'class': 'product-card__body'}):
        try:
            # Znalezienie nazwy produktu
            name = product.find('div', {'class': 'product-card__title'}).text.strip()
            # Znalezienie ceny produktu
            price_text = product.find('div', {'class': 'product-price'}).text.strip()

            # Usuwanie symbolu waluty i konwersja na float
            price_text = price_text.replace('$', '').replace('zł', '').replace(',', '').strip()
            price = float(price_text)

            # Dodanie nazwy i ceny do list
            products.append(name)
            prices.append(price)
        except AttributeError:
            continue
        except ValueError:
            continue

    return products, prices


# Przykładowy URL strony z produktami na Nike
url = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'

# Zbieranie danych
products, prices = get_product_prices(url)

# Tworzenie DataFrame (tabeli) z danymi
df = pd.DataFrame({'Product': products, 'Price': prices})
df.to_csv('nike_product_prices.csv', index=False)
print("Zebrane dane:")
print(df)

# Analiza danych
print("Opis statystyczny danych:")
print(df.describe())

# Wizualizacja danych
plt.figure(figsize=(10, 6))
sns.barplot(x='Product', y='Price', data=df, palette='viridis')
plt.title('Ceny Produktów Nike')
plt.xlabel('Produkt')
plt.ylabel('Cena ($)')
plt.xticks(rotation=90)
plt.show()
