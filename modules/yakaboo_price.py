import re
import requests
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'yakaboo.png')

def yakaboo_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        product_name = soup.find('h1', {'id': 'product-title'}).text.strip()
    except:
        product_name = None

    try:
        price_tag = soup.find('span', {'id': 'product-price'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except:
        price = None

    try:
        old_tag = soup.find('span', {'id': 'product-price-old'}).text.strip()
        old_price = re.sub(r'[^0-9.]', '', old_tag)
    except:
        old_price = None

    if price and old_price:
        try:
            price = float(price)
            old_price = float(old_price)
            discount = round((old_price - price) / old_price * 100, 2)
        except ValueError:
            discount = None
    else:
        discount = None

    try:
        with open(icon_path, 'rb') as f:
            icon = f.read()
    except FileNotFoundError:
        icon = None

    try:
        image_tag = soup.find('img', attrs={'id': 'product-image'})
        image_url = image_tag.get('src')

        # Додаємо протокол, якщо його немає
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('/'):
            image_url = 'https://www.yakaboo.ua' + image_url

        if image_url:
            image_response = requests.get(image_url, headers=headers)
            image = image_response.content
        else:
            image = None
    except:
        image = None
        image_url = None

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    yakaboo_price('https://www.yakaboo.ua/ua/hakeri-i-derzhavi-kibervijni-jak-novi-realii-suchasnoi-geopolitiki.html')
