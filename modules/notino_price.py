import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time, re, requests
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'notino.png')


def notino_price(url):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"

    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        product_name = soup.find('span', class_='sc-3sotvb-3 eUweWP').text.strip()
    except AttributeError:
        product_name = None

    try:
        price_tag = soup.find('span', attrs={'data-testid': 'pd-price'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup.find('span', attrs={'data-testid': 'originalPriceLineThroughWrapper'}).find('span').text.strip()
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
        image_tag = soup.find('div', attrs={'id':'pdImageGallery'}).find('img')
        image_url = image_tag.get('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None
        image_url = None

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image



if __name__ == "__main__":
    notino_price('https://www.notino.ua/armaf/club-de-nuit-men-intense-tualetna-voda-dlja-cholovikiv/')
