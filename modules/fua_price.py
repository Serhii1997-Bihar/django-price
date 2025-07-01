import requests, re, os, time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


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

    soup = BeautifulSoup(response.text, 'html.parser')
    product_name_tag = soup.find('h1')
    product_name = product_name_tag.text.strip() if product_name_tag else None

    try:
        price_tag = soup.find('div', attrs={'class': 'price'}).find_all('div')
        if len(price_tag) > 1:
            actual_price = price_tag[1].text.strip()
        else:
            actual_price = soup.find('div', attrs={'class': 'price'}).text.strip()

        price = float(re.sub(r'[^0-9.]', '', actual_price))
    except (AttributeError, IndexError):
        price = None

    try:
        old_div = soup.find('div', attrs={'class': 'price'}).find_all('div')
        if len(old_div) == 1:
            old_div = None
        else:
            old_div = soup.find('div', attrs={'class': 'price'}).find_all('div')[0]
        old_price = float(re.sub(r'[^0-9.]', '', old_div.text))
    except (AttributeError, IndexError):
        old_price = None

    discount = round((old_price - price) / old_price * 100, 2) if price and old_price else None

    try:
        with open(icon_path, 'rb') as f:
            icon = f.read()
    except FileNotFoundError:
        icon = None

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_path = ChromeDriverManager().install()

    driver = uc.Chrome(
        options=options,
        headless=True,
        driver_executable_path=driver_path)

    driver.get(url)
    time.sleep(3)

    try:
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

    print(product_name, price, old_price, discount, image_url)
    return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    fua_price('https://f.ua/viaplast/butiyl-dlja-vodiy-18-9-litrov.html')
