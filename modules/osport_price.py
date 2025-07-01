import requests, re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'osport.ico')

headers = {
    "authority": "osport.prom.ua",
    "method": "GET",
    "path": "/ua/p551337375-espander-babochka-trenazher.html",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://osport.prom.ua/ua/g10125149-espandery",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0"
}
cookies = {
    "cid": "147608234559237454197010118309394613932",
    "evoauth": "w9bee5213be7b43c790cfec27fd22f343",
    "_ga": "GA1.1.1826121058.1742301606",
    "auth": "84a9b99df4fd05180c0e20ab93933d2924f74602",
    "_gcl_au": "1.1.1655485778.1742301606",
    "_fbp": "fb.1.1742301608708.395864685414168167",
    "csrf_token": "93a2cd2a3f844052940586c697aafccd",
    "visited_products": "2518981448.2485606703.2135690918.1166412076",
    "cto_bundle": "F20nT191bExJTDlrZ0NFWk1JaUNFWFJkajlRQVI4djhSQTkzJTJGWHp2eWxtSlN6OW1KcjUzdVVJczBtWTlnciUyQnJ0MW52R0JiWktHbG55eTc1VHhnYVlRbGRkM0hCMno3dnZkMjAwbHlGaFFqdEdjJTJCMTd6bTJFdUplcmtjUGtVM2lrNm9LWDVZNHpCWE9BSUJqTEhUbER6R24xUHclM0QlM0Q",
    "_ga_F7T5DFHXY0": "GS1.1.1743592738.2.1.1743593322.57.0.0",
    "utmsrc_company_site": "organic",
    "utmcmpg_company_site": "",
    "utmmdm_company_site": "",
    "ext_referer": "aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8=",
    "user_tracker": "043088f116b15a9d6f4cf15838c81e79a990e1a6|188.163.68.19|2025-04-22",
    "csrf_token_company_site": "f7f2deba7dad4d91aaff3617757536b6",
    "companies_visited_products": "551337375.",
    "_ga_T7S2G9Q21Q": "GS1.1.1745339715.1.1.1745340008.0.0.0"
}


def osport_price(url):
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

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'data-qaid':'product-name'}).text.strip()

        try:
            price_tag = soup.find('p', attrs={'data-qaid': 'price-field'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            driver.get(url)
            time.sleep(2)

            html = driver.page_source
            soup_driver = BeautifulSoup(html, 'html.parser')

            old_tag = soup_driver.find('p', attrs={'data-qaid': 'old_product_price'}).text.strip()
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
            image_tag = soup.find('img', attrs={'class': 'Image__image--wFa5m'})
            image_url = image_tag.get('src')
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None


        print(product_name, price, old_price, discount)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    osport_price('https://osport.prom.ua/ua/p1177638435-rezinka-dlya-podtyagivanij.html')