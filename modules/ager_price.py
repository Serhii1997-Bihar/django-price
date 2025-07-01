import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'ager.png')

def ager_price(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,pt;q=0.8",
        "cache-control": "max-age=0",
        "referer": "https://ager.ua/mans/muzhskie-futbolki/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    cookies = {
        "PHPSESSID": "7864974e47c5413e69829264630091d3",
        "language": "en",
        "currency": "UAH",
        "remarketing_cid": "83980311-034b-47dc-a7e6-9f962ee64f25",
        "first_referrer": "www.bing.com",
        "last_referrer": "www.bing.com",
        "_ga": "GA1.1.1882603158.1751189711",
        "_gcl_au": "1.1.1224240387.1751189711",
        "_fbp": "fb.1.1751189711075.217868488246285076",
        "last_visited": "110582",
        "remarketing_ga4_cid": "s1751189710$o1$g1$t1751189729$j41$l0$h764894294",
        "_ga_0W73FCTPT6": "GS2.1.s1751189710$o1$g1$t1751189778$j59$l0$h764894294",
        "biatv-cookie": '{"firstVisitAt":1751189712,"visitsCount":1,"currentVisitStartedAt":1751189712,"currentVisitLandingPage":"https://ager.ua/","currentVisitUpdatedAt":1751189780,"currentVisitOpenPages":4,"campaignTime":1751189712,"campaignCount":1,"utmDataCurrent":{"utm_source":"bing","utm_medium":"organic","utm_campaign":"(not set)","utm_content":"(not set)","utm_term":"(not provided)","beginning_at":1751189712},"utmDataFirst":{"utm_source":"bing","utm_medium":"organic","utm_campaign":"(not set)","utm_content":"(not set)","utm_term":"(not provided)","beginning_at":1751189712}}'
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class':'info-product-block__title'}).text.strip()

        try:
            price_tag = soup.find('div', attrs={'class': 'prise-info-product-block__item_04'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'prise-info-product-block__item_05'}).text.strip()
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
            image_tag = soup.find('img', attrs={'class': 'image-main-product-block__image-small image-main-product-block__image-big zoom-image'})
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount, image_url)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    ager_price('https://ager.ua/238r57832-belyj/')