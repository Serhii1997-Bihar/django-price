import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'shafa.png')

headers = {
    "authority": "brain.com.ua",
    "method": "GET",
    "path": "/ukr/Televizor_Vinga_S24HD25B-p1054579.html",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #"accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://brain.com.ua/ukr/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0"
}
cookies = {
    "PHPSESSID": "e4fnl40mltrdii34caq8okvd5c",
    "Lang": "ua",
    "CityID": "23562",
    "entryRef": "www.bing.com",
    "entryPage": "%2Fukr%2F",
    "_gcl_au": "1.1.641485893.1742386262",
    "_gid": "GA1.3.1433775462.1742386267",
    "sc": "FEAA9DB8-02E8-7699-907B-EF431F6BE9DB",
    "_fbp": "fb.2.1742386266852.565960400519028858",
    "_clck": "1bj9ftt%7C2%7Cfuc%7C0%7C1904",
    "_ga": "GA1.3.386281913.1742386266",
    "biatv-cookie": '{"firstVisitAt":1742386263,"visitsCount":1,"currentVisitStartedAt":1742386263,"currentVisitLandingPage":"https://brain.com.ua/ukr/","currentVisitUpdatedAt":1742386271,"currentVisitOpenPages":2,"campaignTime":1742386263,"campaignCount":1,"utmDataCurrent":{"utm_source":"bing","utm_medium":"organic","utm_campaign":"(not set)","utm_content":"(not set)","utm_term":"(not provided)","beginning_at":1742386263},"utmDataFirst":{"utm_source":"bing","utm_medium":"organic","utm_campaign":"(not set)","utm_content":"(not set)","utm_term":"(not provided)","beginning_at":1742386263}}',
    "_clsk": "t7h428%7C1742386275295%7C2%7C1%7Cl.clarity.ms%2Fcollect",
    "_ga_00SJWGYFLM": "GS1.1.1742386265.1.1.1742386277.48.0.55274427",
    "CityID_Approved": "1"
}


def shafa_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class':'b-product__title'}).text.strip()

        try:
            price_tag = soup.find('span', attrs={'class': 'b-product-price__current'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('span', attrs={'class': 'b-product-price__old'}).text.strip()
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
            image_tag = soup.find('img', attrs={'class': 'b-product-gallery__additional-image'})
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount, image_url)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    shafa_price('https://shafa.ua/women/platya/midi/189363960-suknya-midi-italiya-naturalniy-sklad-rozmir-lxl')