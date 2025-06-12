import re, time, requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'intertop.ico')

def intertop_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"

    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        product_name = soup.find("h2", attrs={"class": "user-product-name"}).text.strip()
    except AttributeError:
        product_name = None

    try:
        price_tag = soup.find("div", attrs={"class": "now-price"}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup.find("div", attrs={"class": "was-price"}).text.strip()
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
        image_tag = soup.find_all('img', attrs={'class':'product-slide__img'})[1]
        image_url = image_tag.get('data-path')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    intertop_price('https://intertop.ua/uk-ua/product/sneakers-puma-9773008')
