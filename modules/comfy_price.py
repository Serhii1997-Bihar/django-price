import requests, re
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'comfy.webp')

headers = {
    "Accept-CH": "viewport-width, width, dpr",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Content-Encoding": "gzip",
    "Content-Type": "text/html; charset=utf-8",
    "Date": "Tue, 18 Mar 2025 11:55:39 GMT",
    "Expires": "0",
    "Feature-Policy": "ch-viewport-width https://scdn.comfy.ua;ch-width https://scdn.comfy.ua;ch-dpr https://scdn.comfy.ua;ch-device-memory https://scdn.comfy.ua;ch-rtt https://scdn.comfy.ua;ch-ect https://scdn.comfy.ua;ch-downlink https://scdn.comfy.ua",
    "Pragma": "no-cache",
    "Referrer-Policy": "no-referrer-when-downgrade",
    "Server": "nginx",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-CDN": "Imperva",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "X-Iinfo": "9-14350543-14350565 NNNY CT(2 3 0) RT(1742298938336 93) q(0 0 0 -1) r(3 3) U12",
    "X-Powered-By": "Express",
    "X-Ray-Id": "TEX51BYAVHM8EFSX36",
    "X-Response-Time": "222",
    "Authority": "comfy.ua",
    "Method": "GET",
    "Path": "/televizor-samsung-ue43du8500uxua.html",
    "Scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "DPR": "1.25",
    "Referer": "https://comfy.ua/flat-tvs/brand__samsung/",
    "Sec-CH-UA": '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    "Sec-CH-UA-Mobile": "?1",
    "Sec-CH-UA-Platform": "Android",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0",
    "Viewport-Width": "591",
}
cookies = {
    "visid_incap_1858972": "YT2nqz6SSQ62VS3onNkydMpd2WcAAAAAQUIPAAAAAAAuT1ce3Z6WqQZ/A8nrYn29",
    "nlbi_1858972": "xrDTfXiaxUie/XuQWvnhXgAAAAAwS29XKnrgInFacFpPBow7",
    "incap_ses_1309_1858972": "RAPJX6opPyDOZ+kgv4AqEspd2WcAAAAAQfU/CKSIZIs6u0UISOgmtw==",
    "ucp_gtm_sid": "9b186291-3400-4fa7-8f67-111a555ae155",
    "_ga": "GA1.1.1372836303.1742298574",
    "action_33443": "RL001024",
    "promo_code_33443": "WISH",
    "xnpe_no_value": "b23b998e-17f4-4200-857c-a68c9ac2d7bd",
    "visid_incap_3129596": "y2OSlifpRca7/f1p66fbJ9Fd2WcAAAAAQUIPAAAAAAAH3UhzJIfviUmrh7KB4SEz",
    "frontend": "ka9fwu11ux7g98dxa7akocdxob",
    "nlbi_3129596": "MRw7HOM2mBcxVdH69cpBZAAAAAD3QtJr3BsQDQZidO9wW2so",
    "incap_ses_688_3129596": "2WWrNrns2XDo27Nol0SMCdFd2WcAAAAAjobW5mJ/wIU67RGMdzUPYg==",
    "cartId": "67d95dd243eb9b796dfde511",
    "_gcl_au": "1.1.664869669.1742298578",
    "userId": "",
    "session_id": "1742298573",
    "_fbp": "fb.1.1742298579460.967122333513212139",
    "__exponea_time2__": "1.0831904411315918",
    "sc": "907939FB-4AE4-0CB3-9F2D-AAFB04426EA1",
    "reese84": "3:r/a4p4lAWHV5/cZegnxbiw==:OOrQoDGRUYt8eApoIUhhuj+DNm3wiogWjkacnBXcbreVnx8X4lBt4rPikB3qoCrUac52K7qvAVMY/nDju9zn37AR+lKoayPrxuvNxeMz5PZX7B4zwVdtisyGgVPBs76iaJIUV8tHfqULVDfh0pSsq8d9sTTYbvo/LInrzR6jGcwrcPYZM/iBLEUIlm0Prljdc7mcC6YpIUlFxgXUugmROoX9tf0w2NAArlBjVQ8khHPTNNolur8lOYvuCLMmuZAMZIs3W9O+oxDMjVCbqviP6GwtaP7RIUnIcMX7dTei5jH6Ob5qZgVev070jPtj9SE69BlIuB/zKAJyWpYN0HMiRFIoDVi18rKaulDru+MgIdMZuXq0rrnW4XQ9+E3r31n9i3A6W3G5o3HOyoXnKYuPHWrknbpCuxsclnuhnb6J6jV4IgZbgZW6/RwIafvG7Vzehz4auh0JXpmRmzvHqQFdlw==:LZ2h4Qbqyaw4ksnT8BQaKnJAs3EKTKXChdZP9UIG1GQ=",
    "customer_group": "0",
    "srv_ab_tst_011": "variantA",
    "xnpe_7d240c70-1f2d-11ee-aac6-eac5edae0088": "d8164909-44fa-470d-857a-1b974eb65e7b",
    "language_popup": "false",
    "_ga_SMJV1PJEMX": "GS1.1.1742298577.1.1.1742298919.0.0.1811008869",
    "_ga_NV2FBMXR21": "GS1.1.1742298578.1.1.1742298919.0.0.1772958157",
    "nlbi_1858972_2147483392": "L1toS1LGIX9y7x5LWvnhXgAAAABr8xRi3jWqTQE0bgMdOU+L",
    "__rtbh.lid": "%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22d7klo0RyhIGCDBaVfbxr%22%2C%22expiryDate%22%3A%222026-03-18T11%3A55%3A19.941Z%22%7D",
    "ucp_uuid": "b23b998e-17f4-4200-857c-a68c9ac2d7bd",
    "__exponea_etc__": "b23b998e-17f4-4200-857c-a68c9ac2d7bd",
    "_uetsid": "1296380003ef11f08bb57f186c9db21d",
    "_uetvid": "12965e6003ef11f0a3ec47ce33d96450",
    "_ga_4XXC45ZSKN": "GS1.1.1742298573.1.1.1742298924.46.0.0",
    "AWSALBTG": "Z8002GnleqHFhLeCkGUKdwPPOUOuOwYeRrJMyqAGVcfzzs3J45IxodA8ejhmhs6/vi2Ss+TykfMAz6IfhS26GPhPFHMMbbe0TP7zU2q2HMT7+q3+hK0DhzTcWgD/rb8MBBpPXUiUnexoqp5Olq59TAz7UVukFNJyLnA8WHkAWei7LB8ZVW0=",
    "AWSALBTGCORS": "Z8002GnleqHFhLeCkGUKdwPPOUOuOwYeRrJMyqAGVcfzzs3J45IxodA8ejhmhs6/vi2Ss+TykfMAz6IfhS26GPhPFHMMbbe0TP7zU2q2HMT7+q3+hK0DhzTcWgD/rb8MBBpPXUiUnexoqp5Olq59TAz7UVukFNJyLnA8WHkAWei7LB8ZVW0=",
    "AWSALB": "hp5sz7bNa+7SRmsYz0WbPr9Y6c+7Oet3o+RkVgCwEMLbcylKbGYxxemWeAhmz8ResUe2acdu+Y/4Lhr3YcpSA5Ee6s6y5yMVSGTMTgnbOczaPjjD4KoH5t3hR4aq",
    "AWSALBCORS": "hp5sz7bNa+7SRmsYz0WbPr9Y6c+7Oet3o+RkVgCwEMLbcylKbGYxxemWeAhmz8ResUe2acdu+Y/4Lhr3YcpSA5Ee6s6y5yMVSGTMTgnbOczaPjjD4KoH5t3hR4aq"
}

def comfy_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class':'gen-tab__name'}).text.strip()

        try:
            price_tag = soup.find('div', attrs={'class': 'price__current'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'price__old-price'}).text.strip()
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
                    attrs={'class': 'gallery__carousel--s fit position-relative'}).find('img')
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    comfy_price('https://comfy.ua/smartfon-xiaomi-15-12-512gb-black.html')