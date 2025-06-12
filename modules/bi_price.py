import requests, re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'bi.png')

def bi_price(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"

    driver.get(url)
    time.sleep(2)

    html = driver.page_source
    soup_driver = BeautifulSoup(html, 'html.parser')

    product_name = soup_driver.find('h1', attrs={'itemprop':'name'}).text.strip()

    try:
        price_tag = soup_driver.find('p', attrs={'itemprop': 'price'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup_driver.find('p', attrs={'class': 'old'}).text.strip()
        cleaned = re.sub(r'[^\d,]', '', old_tag)
        old_price = float(cleaned.replace(',', '.'))
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
        image_tag = soup_driver.find('img', attrs={'class': 'prodImg ac sourceImgJs'})
        image_url = f"https://bi.ua{image_tag.get('src')}"
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    bi_price('https://bi.ua/ukr/product/konstruktor-rastitelnogo-dekora-lego-orhideya-10311.html')