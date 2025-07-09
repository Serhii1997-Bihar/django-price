import time, re, requests
from bs4 import BeautifulSoup
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'laluna.png')

def laluna_price(url):
    headers={"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        product_name = soup.find('h1', attrs={'itemprop':'name'}).text.strip()
    except AttributeError:
        product_name = None

    try:
        price_tag = soup.find('p', attrs={'id': 'formated_price'}).text.strip()
        price = re.sub(r'[^\d]', '', price_tag)
        price = int(price)
    except AttributeError:
        price = None

    try:
        old_tag = soup.find('div', attrs={'class': 'opt_prhhice'}).text.strip()
        old_price = re.sub(r'[^0-9.]', '', old_tag)
    except AttributeError:
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
        image_tag = soup.find('img', attrs={'id': 'image'})
        image_url = image_tag['src']
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image




if __name__ == "__main__":
    laluna_price('https://laluna.com.ua/magazin/jod/kupalnik-bikini-in-849a370')
