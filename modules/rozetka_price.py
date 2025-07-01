import time, re, requests
from bs4 import BeautifulSoup
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'rozetka.ico')

def rozetka_price(url):
    headers={"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Назва товару
    title_tag = soup.find('h1')
    product_name = title_tag.text.strip() if title_tag else None

    # Поточна ціна
    price_tag = soup.find('p', class_='product-price__big')
    price = None
    if price_tag:
        price_text = price_tag.text.strip()
        price = re.sub(r'[^\d.]', '', price_text)
        try:
            price = float(price)
        except ValueError:
            price = None

    # Стара ціна
    old_price_tag = soup.find('p', class_='product-price__small')
    old_price = None
    if old_price_tag:
        old_price_text = old_price_tag.text.strip()
        old_price = re.sub(r'[^\d.]', '', old_price_text)
        try:
            old_price = float(old_price)
        except ValueError:
            old_price = None

    # Знижка
    discount = None
    if price and old_price:
        try:
            discount = round((old_price - price) / old_price * 100, 2)
        except ZeroDivisionError:
            discount = None

    try:
        with open(icon_path, 'rb') as f:
            icon = f.read()
    except FileNotFoundError:
        icon = None

    try:
        image_tag = soup.find('img', attrs={'class': 'object-contain'})
        image_url = image_tag.get('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image




if __name__ == "__main__":
    rozetka_price('https://rozetka.com.ua/ua/365448825/p365448825/')
