import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'moyo.png')

headers = {
    "authority": "www.moyo.ua",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "referer": "https://www.moyo.ua/ua/comp-and-periphery/noutebook_pc/comp/",
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
    "PHPSESSID": "4l3c0nu03oh7e21q7tvn1r6839",
    "lang": "uk_UA",
    "cityActiveId": "3390",
    "basket": "b9a942b867d5f7df05f9c45e9e5da8aa",
    "basket_summary_products": "0",
    "basket_summary_money": "0",
    "isContextQuery": "0",
    "YII_CSRF_TOKEN": "NE9pX25Cdk16VmZXcEV5eTZBVHRTSG1lc2J1bGR2NTHfO5V1iY7DfOs-ZMHEZYjs2KYkKoA-XlgsSpouUqcs9g==",
    "_gcl_au": "1.1.1981229726.1743443114",
    "source": "sourceCookie|utm_source",
    "sc": "35D3969F-BFE1-42CB-F208-28843E1C8691",
    "_omappvp": "HLIf3ZcsZtAgbR8LRyoCAKBkzNryRnejnlYNYyPxQdO2JBKDns6gt43lQYZcVZlmQAUMTIR3eRH3l5pHdGq35JqAB5kcbwoA",
    "_omappvs": "1743443115485",
    "_gid": "GA1.2.206905023.1743443116",
    "__utma": "46025016.199768111.1743443116.1743443116.1743443116.1",
    "__utmc": "46025016",
    "__utmz": "46025016.1743443116.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "__utmt_UA-16250353-8": "1",
    "__utmb": "46025016.1.10.1743443116",
    "__rtbh.uid": '{"eventType":"uid","id":"undefined","expiryDate":"2026-03-31T17:45:15.908Z"}',
    "__rtbh.lid": '{"eventType":"lid","id":"3D7Z1BR4pH1Ai2rx08Vp","expiryDate":"2026-03-31T17:45:15.910Z"}',
    "__user_id": "uid-2749513070.4012770111",
    "_hjSessionUser_1850514": "eyJpZCI6ImNlMGIxZDI1LTA3YjctNTk3ZC05ZDZmLTFmOWE3NGYzM2E2MSIsImNyZWF0ZWQiOjE3NDM0NDMxMTYyNDcsImV4aXN0aW5nIjpmYWxzZX0=",
    "_hjSession_1850514": "eyJpZCI6ImI4OTQ4YzkwLTc2YzUtNDI5Yi04NWI4LTQ3NWVlNmZiNzczNyIsImMiOjE3NDM0NDMxMTYyNDksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MX0=",
    "_fbp": "fb.1.1743443116641.131411958536954155",
    "_dc_gtm_UA-16250353-2": "1",
    "_ga": "GA1.2.199768111.1743443116",
    "_clck": "dk0uzr|2|fuo|0|1916",
    "biatv-cookie": '{"firstVisitAt":1743443114,"visitsCount":1,"currentVisitStartedAt":1743443114,"currentVisitLandingPage":"https://www.moyo.ua/ua/portal_brand/comp_and_periphery/","currentVisitUpdatedAt":1743443114,"currentVisitOpenPages":1,"campaignTime":1743443114,"campaignCount":1,"utmDataCurrent":{"utm_source":"(direct)","utm_medium":"(none)","utm_campaign":"(direct)","utm_content":"(not set)","utm_term":"(not set)","beginning_at":1743443114},"utmDataFirst":{"utm_source":"(direct)","utm_medium":"(none)","utm_campaign":"(direct)","utm_content":"(not set)","utm_term":"(not set)","beginning_at":1743443114}}',
    "_clsk": "b5wf06|1743443117718|1|1|l.clarity.ms/collect",
    "_ga_J9PXXCD8FY": "GS1.1.1743443115.1.0.1743443149.0.0.994305841",
    "_ga_2YP56NYVCH": "GS1.1.1743443115.1.0.1743443149.0.0.1412262205",
    "new_user_ga": "1",
    "no_detected_user_ga": "0",
    "publicKey": "d506f4607387f1af0c65035d118e5f4d",
    "dl_meta": '{"auth_cid":"199768111.1743443116"}'
}



def moyo_price(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class': 'product_name', 'itemprop': 'name'}).text.strip()

        try:
            price_tag = soup.find('div', attrs={'class': 'product_price base-product_price'}).find('span').text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'product_price_oldprice base-product_price_oldprice js-old-price'}).text.strip()
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
            image_tag = soup.find('div',
                attrs={'id': '34cb71d0-d649-4608-98aa-0cebd2069e24'}).find('img')
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    moyo_price('https://www.moyo.ua/ua/sistemnyyi_blok_2e_rational_2e-2600/480394.html')
