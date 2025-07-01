import requests, re
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os, time
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'eldorado.ico')

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://www.google.com/",
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
    "userGUID": "54eb4410-1f73-11f0-a4a4-edc4212153be",
    "ABtesting": "not_set",
    "ModalLeftProductsStatus": "available",
    "_gcl_au": "1.1.677748959.1745324063",
    "thxPage": "undefined",
    "sc": "60BD74E2-36E1-EF04-8898-A63ABADE6C38",
    "lfp": "4/22/2025, 3:14:23 PM",
    "lang": "uk",
    "_ga": "GA1.2.141010211.1745324066",
    "_gid": "GA1.2.381085200.1745324066",
    "pa": "1745324066175.88330.8072109934252777eldorado.ua0.3655714323620184+1",
    "_hjSessionUser_755824": "eyJpZCI6IjA5OTEzNjEwLTlkYzAtNTE5Yy04M2U0LTExZDNmNmY3ODc0YyIsImNyZWF0ZWQiOjE3NDUzMjQwOTM3MTcsImV4aXN0aW5nIjpmYWxzZX0=",
    "_hjSession_755824": "eyJpZCI6IjkyNDgyZmVhLTkwYTUtNGJmYy1hNTExLTBjZWNlNjAxMmEyNCIsImMiOjE3NDUzMjQwOTM3MTksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=",
    "eldorado": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJndWVzdCIsInN1YiI6InNlc3Npb25JZF8zYTg3NGJmNy03NDk5LTRkZjctOGY5MC0xZDU3M2YxODU1ZTEiLCJpYXQiOjE3NDUzMjQwOTYsImV4cCI6MTc0NjUzMzY5Nn0.tm6Tp06wauLTLfpIEtcfMg7pTtb5_CGNILXGPLeCtYg",
    "fp": "4",
    "_ga_RT2TZS3S91": "GS1.2.1745324067.1.1.1745324100.27.0.0",
    "_ga_B38R3NX8B4": "GS1.1.1745324065.1.1.1745324100.25.0.0",
    "_fbp": "fb.1.1745324100766.51186073251725161"
}


def eldorado_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    driver.get(url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    product_name = soup.find('div', attrs={'itemprop':'name'}).text.strip()

    try:
        price_tag = soup.find('div', attrs={'class': 'price-value difference'}).find_next('span', attrs={'class':'value'}).text.strip()
        price = re.sub(r'[^0-9.]', '', price_tag)
    except AttributeError:
        price = None

    try:
        old_tag = soup.find('div', attrs={'class': 'old-price-value'}).text.strip()
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
        image_tag = soup.find('img', attrs={'id': 'image-magnify-img'})
        image_url = image_tag.get('src')
        if image_url:
            image_response = requests.get(image_url)
            image = image_response.content
    except AttributeError:
        image = None

    print(product_name, price, old_price, discount)
    return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    eldorado_price('https://eldorado.ua/uk/kavovarka-cecotec-cafelizzia-790-steel-cctc-01582/p71335340/')