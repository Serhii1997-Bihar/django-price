import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'deca.ico')

headers = {
    "authority": "deka.ua",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #"accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://www.google.com/",
    "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0"
}
cookies = {
    "SALE_AFFILIATE": "1000",
    "SALE_AFFILIATE_SET_DATE": "1744800698",
    "guestId": "10620404",
    "_gcl_gs": "2.1.k1$i1744800700$u168011828",
    "_gcl_au": "1.1.1022426490.1744800702",
    "sbjs_migrations": "1418474375998%3D1",
    "sbjs_current_add": "fd%3D2025-04-16%2013%3A51%3A42%7C%7C%7Cep%3Dhttps%3A%2F%2Fdeka.ua%2F%3Fgad_source%3D1%26gclid%3DCj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
    "sbjs_first_add": "fd%3D2025-04-16%2013%3A51%3A42%7C%7C%7Cep%3Dhttps%3A%2F%2Fdeka.ua%2F%3Fgad_source%3D1%26gclid%3DCj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F",
    "sbjs_current": "typ%3Dutm%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dcpc%7C%7C%7Ccmp%3Dgoogle_cpc%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "sbjs_first": "typ%3Dutm%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dcpc%7C%7C%7Ccmp%3Dgoogle_cpc%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29",
    "sbjs_udata": "vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Safari%2F537.36%20Edg%2F135.0.0.0",
    "sbjs_session": "pgs%3D1%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fdeka.ua%2F%3Fgad_source%3D1%26gclid%3DCj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB",
    "_gcl_aw": "GCL.1744800703.Cj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB",
    "__rtbh.lid": '{"eventType":"lid","id":"tZMcL44eEfiguJqsKR2D","expiryDate":"2026-04-16T10:51:42.756Z"}',
    "sc": "350A67D6-079A-637F-4869-D1EC82A03431",
    "_fbp": "fb.1.1744800703224.77211432461382328",
    "_ga": "GA1.2.1268073300.1744800703",
    "_gid": "GA1.2.337250463.1744800703",
    "_gac_UA-3103127-3": "1.1744800703.Cj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB",
    "_gac_UA-3103127-7": "1.1744800703.Cj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB",
    "_gac_UA-3103127-9": "1.1744800703.Cj0KCQjwqv2_BhC0ARIsAFb5Ac9A1ebASDUeAkh5w80ioBiBiKkD1eUJg2eRXmeUXLPECkVcVx_b7HYaAmJYEALw_wcB",
    "_tt_enable_cookie": "1",
    "_ttp": "01JRZ3KSCTB8YT34QQ6PQKT9T1_.tt.1",
    "_ga_L5BC01QHFV": "GS1.2.1744800704.1.1.1744801356.22.0.0",
    "_ga_SFKPSSKG55": "GS1.2.1744800704.1.1.1744801356.0.0.0",
    "ttcsid": "1744800703913.1.1744801356461",
    "__rtbh.uid": '{"eventType":"uid","id":"unknown","expiryDate":"2026-04-16T11:02:36.877Z"}',
    "ttcsid_C4NK4LHPGM656MIK2SE0": "1744800703909.1.1744801357338",
    "_ga_DHZR06XDFD": "GS1.1.1744800702.1.1.1744801357.21.0.747295876"
}


def deka_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class':'blocks-product-heading__title'}).text.strip()

        try:
            price_tag = soup.find('div', attrs={'class': 'blocks-product-order__price'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'blocks-product-order__old-price'}).text.strip()
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
            image_tag = soup.find('img',
                        attrs={'class': 'product-side-slide__image'})
            image_url = image_tag.get('src')
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    deka_price('https://deka.ua/ua/fossil-jf-00659-791-12.html')