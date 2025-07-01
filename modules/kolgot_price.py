import requests, re, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'kolgot.png')

def kolgot_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    try:
        product_name = soup.find('h1').text.strip()
    except AttributeError:
        product_name = None

    try:
        price_tag = soup.find('div', attrs={'class': 'container-price-and-model'}).find_all('ul')[1]
        price_li = price_tag.find_all('li')[1].text.strip()
        price = re.sub(r'[^0-9.]', '', price_li)
    except (AttributeError, IndexError):
        price = None

    try:
        old_tag = soup.find('div', attrs={'class': 'container-price-and-model'}).find_all('ul')[1]
        old_li = old_tag.find_all('li')[0].text.strip()
        old_price = re.sub(r'[^0-9.]', '', old_li)
    except (AttributeError, IndexError):
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
        image_tag = soup.find('img', attrs={'title': product_name})
        image_url = image_tag['src']
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
        else:
            image = None
    except AttributeError:
        image_url = None
        image = None

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    kolgot_price('https://kolgot.net/ua/fantaziyni-kolhotky-z-imitatsiyeyu-panchikh-iz-poyasom-pari-lurex-60-4-giulia-nero-chornyy')
