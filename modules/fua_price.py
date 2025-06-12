import requests, re, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'fua.ico')

headers = {
    "referer": "https://makeup.com.ua/ua/categorys/3218/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0"
}


def fua_price(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None, None, None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    product_name_tag = soup.find('h1')
    product_name = product_name_tag.text.strip() if product_name_tag else None

    try:
        price_tag = soup.find('div', attrs={'class': 'price'})
        price_divs = price_tag.find_all('div') if price_tag else []
        actual_price = price_divs[1].text.strip() if len(price_divs) > 1 else None
        price = float(re.sub(r'[^0-9.]', '', actual_price)) if actual_price else None
    except Exception:
        pass

    try:
        old_divs = price_tag.find_all('div') if price_tag else []
        actual_old_price = old_divs[0].text.strip() if old_divs else None
        old_price = float(re.sub(r'[^0-9.]', '', actual_old_price)) if actual_old_price else None
    except Exception:
        old_price = None

    discount = round((old_price - price) / old_price * 100, 2) if price and old_price else None

    try:
        with open(icon_path, 'rb') as f:
            icon = f.read()
    except FileNotFoundError:
        icon = None

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        image_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'li.swiper-slide.swiper-slide-active picture img')))
        image_url = image_element.get_attribute('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except Exception as e:
        print(f"Image fetch error: {e}")
        image = None
    finally:
        driver.quit()

    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    fua_price('https://f.ua/vitals/tachka-odnokolesnaja-65-110-4m.html')
