import requests, re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import os, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'answear.png')

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,pt;q=0.8",
    "cache-control": "max-age=0",
    "referer": "https://answear.ua/c/vona?ref=admitad.com&utm_source=admitad&utm_medium=affiliate&utm_campaign=channable&utm_term=119134&admitad_uid=136b2e2829b56ac354a8efc825aac16f&publisher_id=119134&website_id=2600679&channel_id=&group_id=&tagtag_uid=136b2e2829b56ac354a8efc825aac16f",
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
    "user_country_code": "UA",
    "ak_bmsc": "24CAE55538F176529366369AAA426727~000000000000000000000000000000~YAAQTb17XC51gcaXAQAAo74B1hz8ctH6/iwJUmpd5MOD/vCCIz7dINaY9npmlrSOftZK/nqb3lVFX1aH2meZ+9Dp7l9IKLxytcWMa2XH8q2A4xxdCYirgI1/Rds/lh2wQqom8qChnQ5AvewEIp4DjJus3vhLeJtteE0ngLLZWYdaL2D+i+i89ai/qd16mVJAGL3Vt6z7k+zqtNx5HpVoFv9Hp5hn/DOy1QeBjk5TLN7FEku0qcn45vzUw3zoM7dKxumSRCbyi1TpfNaGtB9qdhruPSq3stW0t+Hx09gSXWEqYhlzlFGCjNWlRt9n020ECGXVGsUxM8RddZiBY6dijiHvtWgOozO8Q4igQ3foVOlvNaDGR0KA78HZsr66EZwznSYBVSoNfI/p3w==",
    "selectedHomepage": "female",
    "selectedLanguage": "uk_UA",
    "ab.storage.sessionId.557e2237-265d-4d0e-9768-7b110e3450da": "g%3A3ead35f4-2311-e010-258d-c87028e8f45c%7Ce%3A1751643985082%7Cc%3A1751642185082%7Cl%3A1751642185082",
    "ab.storage.deviceId.557e2237-265d-4d0e-9768-7b110e3450da": "g%3A9bfc8d2d-c8ca-2ef7-3362-2ac0129269d2%7Ce%3Aundefined%7Cc%3A1751642185088%7Cl%3A1751642185088",
    "_lb": "7523245908923402000",
    "user_first_visit": "2025-07-04",
    "user_group": "uncategorized",
    "CookieConsent": "1%2C1%2C1%2C1",
    "_gcl_au": "1.1.948128416.1751642794",
    "_ga": "GA1.1.1007962248.1751642188",
    "FPID": "FPID2.2.jAp1kgI3dYYdDnNgFqJGht8DR%2FXvFCnkjxqgcQdTWT4%3D.1751642188",
    "FPAU": "1.1.948128416.1751642794",
    "referrer": "answear.ua",
    "FPLC": "bdBUsBgEvIGQTpyHiCLENvHCkFEu9XaP3UB7tMw2QImQ%2BUdKGaHzFCKfT%2BU%2B7HXKmkhMiDAYevUHCsqhDDW5S20C7jW1dYV8ZV3UC9Am6OEOTBfg%2BWLtra%2FsDtTPWQ%3D%3D",
    "_lb_id": "7523245908923402000",
    "_lb_ccc": "1",
    "__rtbh.lid": "{\"eventType\":\"lid\",\"id\":\"hlYbss5rzJN5Rx8Y8dn4\",\"expiryDate\":\"2026-07-04T15:26:34.930Z\"}",
    "_gtmeec": "e30%3D",
    "_dcid": "dcid.1.1751642794639.548178431",
    "_fbp": "fb.1.1751642794648.1394986121",
    "_tt_enable_cookie": "1",
    "_ttp": "01JZB0QV5VB9C1VBBFGNF6YP1Z_.tt.1",
    "_clck": "e9hlwm%7C2%7Cfxb%7C0%7C2011",
    "cto_bundle": "ALZgyl9ZelNsclJmWXFzRXFSY1ppOHZ6RlN5MFRybmdnUm5oT3NvOTlIZEEzbnpMbTBzV0NwWW02dEpSMUlWSVpFWlMlMkJ1a0UlMkJ3SyUyRjlPd1VPTVZRV0JXeEQ1MGJBSmNDTGE5Wno4JTJCd0pnZlloUjFtUTdGOFhxMU14JTJCd1gwT1c0SXZ6dXo3aVpDN0p4ZiUyQlV1UEpDT0ZaJTJCdjRaUSUzRCUzRA",
    "_hjSessionUser_2205215": "eyJpZCI6ImJkZjNlNmUwLTk0ZTAtNWViNS1hMDg4LWU4YmNlNzA0YzRjNCIsImNyZWF0ZWQiOjE3NTE2NDI3OTkzNDgsImV4aXN0aW5nIjpmYWxzZX0=",
    "_hjSession_2205215": "eyJpZCI6IjVkMzJhMmQ5LTk5YWItNDRlOC1iMjc3LTM1ODFlY2VkM2JlOSIsImMiOjE3NTE2NDI3OTkzNTAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
    "_HC_fr": ":::1751642807",
    "_HC_uu": "O5TmhvA1PfHrb-2Ozzzzzzzz",
    "_clsk": "17hdcll%7C1751642904509%7C7%7C1%7Cl.clarity.ms%2Fcollect",
    "__rtbh.uid": "{\"eventType\":\"uid\",\"id\":\"undefined\",\"expiryDate\":\"2026-07-04T15:28:25.008Z\"}",
    "_uetsid": "455d72e058eb11f0b087cda0f154aa54",
    "_uetvid": "455deef058eb11f082ef29c656cc9056",
    "ttcsid": "1751642795216::ARuioAiNBkMc3YzR9eME.1.1751642905816",
    "ttcsid_CCOPKSBC77UB1O51K5HG": "1751642795214::FEj9MSfk38wwFz4xloRV.1.1751642905982",
    "_HC_v4793": "BWhn8rcABQBi~O5TmhvA1PfHrb-2O",
    "RT": "z=1&dm=answear.ua&si=8c5020d6-7215-460c-9fdc-0304b2a6e7ad&ss=mcoyif86&sl=7&tt=dyuf&bcn=%2F%2F0217991b.akstat.io%2F&nu=18a5a8cjh&cl=g3bz&ld=g5q7",
    "_ga_CLD0D8MZFJ": "GS2.1.s1751642188$o1$g1$t1751643084$j23$l0$h1902009346",
    "_ga_40Q5TCMMEF": "GS2.1.s1751642188$o1$g1$t1751643084$j23$l0$h0"
}


def answear_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1').find('span').text.strip()

        try:
            price_tag = soup.find('div', attrs={'class': 'ProductCard__priceSale__dDB+o'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'ProductCard__priceRegularWithSale__VMmoN'}).text.strip()
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
            image_tag = soup.find('picture', attrs={'class': 'Image__cardImage__AMJQB'}).find('img')
            image_url = image_tag['src']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        print(product_name, price, old_price, discount, image_url)
        return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    answear_price('https://answear.ua/p/llyanyj-kombinezon-united-colors-of-benetton-kolir-zelenyj-dekolte-trykutnyk-4aghdt00e-1532202')