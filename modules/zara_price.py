import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time, re, requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'zara.png')


def zara_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    product_name = soup.find('h1').text.strip()

    try:
        price_tag = soup.find('span', attrs={'class': 'money-amount__main'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup.find('div', attrs={'class': 'card__price-old'}).text.strip()
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
        image_tag = soup.find('img', attrs={'class': 'media-image__image media__wrapper--media'})
        image_url = image_tag.get('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None


    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    zara_price(
        'https://www.zara.com/ua/uk/-%D1%82-%D0%B5-%D0%BA-%D1%81-%D1%82-%D1%83-%D1%80-%D0%BE-%D0%B2-%D0%B0-%D0%BD-%D0%B0---%D1%81-%D0%BE-%D1%80-%D0%BE-%D1%87-%D0%BA-%D0%B0---%D0%BF-%D0%BE-%D0%BB-%D0%BE--p02688106.html?v1=442465392&v2=2544454')
