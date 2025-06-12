import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, re, requests
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'citrus.png')

def citrus_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium-browser" #snap
    driver = uc.Chrome(options=options, driver_executable_path="/usr/bin/chromium-browser")
    # driver_executable_path="/usr/bin/chromedriver"
    try:
        driver.get(url)
        time.sleep(3)

        try:
            product_name = driver.find_element(By.XPATH, "//h1[@class='DescriptionTitle_title__PxMkv']").text.strip()
        except:
            product_name = None

        try:
            price_tag = driver.find_element(By.XPATH, "//div[@class='price medium no-wrap f-secondary Price_price__KKCnw']").text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except:
            price = None

        try:
            old_tag = driver.find_element(By.XPATH, "//div[@class='old-price old-price--error mr24 f-secondary OldPrice_oldPrice__tON_E']").text.strip()
            old_price = re.sub(r'[^0-9.]', '', old_tag)
        except:
            old_price = None

        try:
            discount = round((int(old_price) - int(price)) / int(old_price) * 100, 2) if old_price and price else None
        except:
            discount = None

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            with open(icon_path, 'rb') as f:
                icon = f.read()
        except FileNotFoundError:
            icon = None

        try:
            image_tag = soup.find_all('img', attrs={'class': 'ProductSlider-module__image___1qhoG'})[1]
            image_url = image_tag['src']
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image = image_response.content
                driver.quit()
            else:
                image = None
        except AttributeError:
            image = None

    finally:
        driver.quit()

    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    citrus_price(
        'https://www.ctrs.com.ua/morozilnye-kamery/morozilnaya-kamera-gorenje-fn619fes5-712485.html')
