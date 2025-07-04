import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re, time, requests
from bs4 import BeautifulSoup
import os
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'yakaboo.png')

def yakaboo_price(url):
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
    soup = BeautifulSoup(html, 'html.parser')

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
        image_url = image_tag['src']
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    finally:
        driver.quit()

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    yakaboo_price('https://www.yakaboo.ua/ua/ozero-spokoju-limited-edition.html')
