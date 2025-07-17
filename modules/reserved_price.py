import requests, re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os, time
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'reserved.ico')

def reserved_price(url):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_path = ChromeDriverManager().install()

    driver = uc.Chrome(
        options=options,
        headless=True,
        driver_executable_path=driver_path
    )

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup_driver = BeautifulSoup(html, 'html.parser')

    product_name = soup_driver.find('h1', attrs={'data-testid':'product-name'}).text.strip()

    try:
        price_tag = soup_driver.find('div', attrs={'data-selen': 'product-discount-price'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup_driver.find('div', attrs={'data-selen': 'product-regular-price'}).text.strip()
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
        image_tag = soup_driver.find('img', attrs={'class': 'sc-gsBqHK jPpeIL'})
        image_url = image_tag.get('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    print(product_name, price, old_price, discount)
    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    reserved_price('https://www.reserved.com/ua/uk/shkiriana-kurtka-7177h-99x')