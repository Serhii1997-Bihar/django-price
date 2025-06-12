import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time, re, requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'allo.png')

def allo_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        product_name = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.strip()
    except:
        product_name = None

    try:
        price_tag = driver.find_element(By.XPATH, "//div[@itemprop='offers']//span[@class='sum']").text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except:
        price = None

    try:
        old_tag = driver.find_element(By.XPATH, "//div[@class='p-trade-price__old']//span[@class='sum']").text.strip()
        old_price = re.sub(r'[^0-9.]', '', old_tag)
    except:
        old_price = None

    try:
        discount = round((int(old_price) - int(price)) / int(old_price) * 100, 2) if old_price and price else None
    except:
        discount = None

    icon = None
    try:
        icon_tag = driver.find_element(By.XPATH, "//link[@rel='apple-touch-icon']")
        icon_url = icon_tag.get_attribute("href")
        if icon_url:
            icon_response = requests.get(icon_url)
            icon = icon_response.content
    except:
        icon_url = None

    try:
        source = soup.find('div', attrs={'class':'p-view__main'}).find_all('source')
        image_url = source[1].get('srcset')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    finally:
        driver.quit()

    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    print(allo_price('https://allo.ua/ua/televizory/televizor-xiaomi-tv-a-43-fhd-2025.html'))

