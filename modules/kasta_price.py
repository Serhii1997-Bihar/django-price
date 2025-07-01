import requests, re
from bs4 import BeautifulSoup

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'kasts.ico')

def kasta_price(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,pt;q=0.8",
        "cache-control": "max-age=0",
        "referer": "https://kasta.ua/uk/market/odezhda~affiliation_zhinkam~kind_kupalynik/",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    cookies = {
        "ab_discount_test": "0",
        "kcid": "Xr7o_Cmdqs",
        "sbjs_migrations": "1418474375998=1",
        "sbjs_current_add": "fd=2025-06-29 11:19:43|||ep=https://kasta.ua/|||rf=https://www.bing.com/",
        "sbjs_first_add": "fd=2025-06-29 11:19:43|||ep=https://kasta.ua/|||rf=https://www.bing.com/",
        "sbjs_current": "typ=referral|||src=bing.com|||mdm=referral|||cmp=(none)|||cnt=/|||trm=(none)",
        "sbjs_first": "typ=referral|||src=bing.com|||mdm=referral|||cmp=(none)|||cnt=/|||trm=(none)",
        "sbjs_udata": "vst=1|||uip=(none)|||uag=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "_gcl_au": "1.1.927062476.1751185184",
        "firebase_au": "1.1.1000915360.1751185185",
        "firebase_ga": "GA1.1.723802892.1751185185",
        "_gid": "GA1.2.1012464861.1751185185",
        "_tt_enable_cookie": "1",
        "_ttp": "01JYXCARRY00N7J7WAFV3N8SZ7_.tt.1",
        "cebs": "1",
        "_ce.clock_data": "-666,188.163.68.19,1,d2ad6785d256851dd366703bdc61aa61,Edge,UA",
        "_ce.s": "v~f7968d11b162f971d6846efbbc97b7ba86b832d1~lcw~1751185197519~vir~new~lva~1751185216179~vpv~0~v11.cs~453802~v11.s~d23c8bd0-54c1-11f0-a284-ef9fcab46bb1~v11.vs~f7968d11b162f971d6846efbbc97b7ba86b832d1~v11.fsvd~eyJ1cmwiOiJrYXN0YS51YSIsInJlZiI6Imh0dHBzOi8vd3d3LmJpbmcuY29tLyIsInV0bSI6W119~v11.ss~1751185188122~v11ls~d23c8bd0-54c1-11f0-a284-ef9fcab46bb1~v11nv~0~lcw~1751185216179",
        "_fbp": "fb.1.1751185216325.411367259968468306",
        "_dc_gtm_UA-17567430-1": "1",
        "cto_bundle": "MNZlAV9uZ2NjWDl4JTJGOVVQWnolMkJLNyUyQmFTT2JnRVBjTEJmcUxYaG5iZ2w5R3dCMmxTYVlROUZRUGxIZjBqc1d0TzRWJTJGNXo5RkVzdmJtdTVZVngyc2xsTWFBQkFSNkcxUnkxVXVRdXB5Z2ViRG1keVFJMFl3SlFvVTVhODZwSHhTWnV0WXNKc0R3NHpZQTNqV2tLaWxNQ1NaeTZBZyUzRCUzRA",
        "sbjs_session": "pgs=8|||cpg=https://kasta.ua/uk/product/18220953:623/",
        "_ga_MSTJ696GVD": "GS2.1.s1751185184$o1$g1$t1751185364$j55$l0$h0",
        "_ga_Y84B01ZD7Z": "GS2.1.s1751185185$o1$g1$t1751185364$j55$l0$h0",
        "_ga": "GA1.2.723802892.1751185185",
        "cebsp_": "8",
        "__rtbh.lid": "{\"eventType\":\"lid\",\"id\":\"uqtUWNARE53SkvQCR43H\",\"expiryDate\":\"2026-06-29T08:22:45.932Z\"}",
        "chua_session": "[\"nsULj8x4HS2\",1751185366075]",
        "__rtbh.uid": "{\"eventType\":\"uid\",\"id\":\"undefined\",\"expiryDate\":\"2026-06-29T08:22:46.152Z\"}",
        "firebase_ga_1Z132N00BH": "GS2.1.s1751185184$o1$g1$t1751185369$j39$l0$h1089134480",
        "ttcsid": "1751185187630::XasbO-3YyNjcHE-OT1eE.1.1751185370008",
        "ttcsid_D09HOB3C77UF1HSAKS4G": "1751185187629::0eLx8uID_ZpXBYLVbx4k.1.1751185373686",
        "g_state": "{\"i_p\":1751192582663,\"i_l\":1}"
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_name = soup.find('h1', attrs={'class':'p__pads p__title p__name m-0'}).text.strip()

        try:
            price_tag = soup.find('span', attrs={'id':'productPrice'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('span', attrs={'id':'productOldPrice'}).text.strip()
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
            image_tag = soup.find('img', attrs={'class': 'aspect-inner'})
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount, image_url)
        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    kasta_price('https://kasta.ua/uk/product/18220953:623/')