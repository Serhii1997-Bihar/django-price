import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'prom.png')

def prom_price(url):
    headers = {
        "authority": "prom.ua",
        "method": "GET",
        "path": "/ua/p2119971872-eroticheskij-kostyum-shkolnitsa.html",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,pt;q=0.8",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://prom.ua/ua/Zhenskoe-eroticheskoe-bele",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "service-worker-navigation-preload": "true",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }

    cookies = {
        "cid": "294721937844641236240272526392348869897",
        "evoauth": "w92de5bcfe05e450f84adf77cb7375a19",
        "timezone_offset": "180",
        "_ga": "GA1.1.1541502819.1751175258",
        "last_search_term": "",
        "auth": "cac69554ab450208aa40500704c69973ed3fb9fd",
        "_gcl_au": "1.1.1957462486.1751175259",
        "postAuthQueue": '[{%22key%22:%22forceUpdateBesidaUser%22}]',
        "user_tracker": "5cb563740c72e2f30f8dc542153139ef4e3a1dcd|188.163.68.19|2025-06-29",
        "csrf_token": "b78917c521de471cb2af3a484f0422db",
        "cookie_storage": '{%22clientId%22:%22c-TCY6ugvk4wPdiO0bwoCoTKlK%22%2C%22isMaybeProductsInCart%22:false}',
        "adult_user": "true",
        "_fbp": "fb.1.1751175302837.35599604691398774",
        "visited_products": "2119971872",
        "cto_bundle": "Pb_EBV9uZ2NjWDl4JTJGOVVQWnolMkJLNyUyQmFTT2JrYUJCeHQ3bWpadEFNalElMkZHODZzUEoyYWxmTjlXOXJ6ak1VZEgzMEFhdmxURXZQMUhkR0xnbTJwM09UUzRrQjJvYVgxODFxNU5oMDN6cFVBZzhmR0tsQk9NY2tPdXQ2cGYxJTJGYjExbCUyRjVwRURscmt5UkJUNVo0UkQ3TGhpd0xDQmclM0QlM0Q",
        "__rtbh.uid": '{"eventType":"uid","id":"unknown","expiryDate":"2026-06-29T05:36:27.362Z"}',
        "__rtbh.lid": '{"eventType":"lid","id":"vX5zQQXHFLebfpRvnqML","expiryDate":"2026-06-29T05:36:27.362Z"}',
        "wasProductCardVisited_2119971872": "true",
        "_ga_F7T5DFHXY0": "GS2.1.s1751175257$o1$g1$t1751175472$j32$l0$h0"
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        product_name = soup.find('h1', attrs={'data-qaid':'product_name'}).text.strip()

        try:
            price_tag = soup.find('div', attrs={'class':'MafxA sMS5m'}).find('div', attrs={'data-qaid': 'product_price'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class':'MafxA sMS5m'}).find('span', attrs={'data-qaid': 'old_price'}).text.strip()
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
            image_tag = soup.find('img', attrs={'data-qaid': 'image_preview'})
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount, image_url)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    prom_price('https://prom.ua/ua/p2506530614-noutbuk-lenovo-ideapad.html')