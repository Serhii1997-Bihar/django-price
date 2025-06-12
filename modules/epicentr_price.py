import requests, re
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'epicentr.webp')

headers = {
    "authority": "epicentrk.ua",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "referer": "https://epicentrk.ua/",
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
    'PHPSESSID': 'q89dmpor8n2gia2c4vttbqagk6e9061ihuca7tlr',
    'LANG_CHANGE_REQUIRE': '0',
    'LANG': 'ua',
    'EPIC_LANG': 'ua',
    'LANG_SUBDOMAIN': 'ua',
    'AB_TEST_DVA_SLIDER_V5': '1',
    'BITRIX_SM_LOCATION': 'def502005306a2e6d621131f8faca6ccedf8cdc4183be9f868fc7555ff7863fcaf22b7bffc5de3b9911e77e0d53f257fd10d66b1218ea13bf03e045b80a65b7d5e6a679ca8aa542d2e6327e898a4a52c7f88dcf3c1b08ed4c02930ce673a64306a3a82adbbd26946599483b0c237e395511396b3e4737857347fd5b7b0b3c3f36fb0f4919ff804f1e5f4a707f789faf143201f4c7344648dd79daf22bc9b872d65c8d930402579eba10af5a35e6e01291f38a43e590265b38f93e701805c774a3efe601aca7517a94fd55bea28918b489e6b5d9f9e8b6f4a4a9cd49daff6d914744c080c62faccdbc2eea334932bd3ec7b2ebb67e751f81c01c56a78662af63f77e247aa92fd29cffe8fd5380731d5c14b562ce1ad355d0adefb913d42e0e8d56b956046a209ebc260c983bb066e72226d0686e595863a6fa5661fa21f7bdf277bc99f78e34e40efe13af9ff1685b067e9325862c5970280919cda23fb59b00a6afb6152a3d8e301dfc1be4264d2e0032de10a95d0ded2935f18d63088a1839e52645cc714c8938f8709f525333e60cf3e3baa487b92e9d470d40cd7219cef7306343ac9695e04207a5de9135e888862d39013da32843500bfb197cc7b5b597c262a0fcd8e098a2012037c8185e7ef885a5578f869bf6db2787382a39da80e0aedf94a12a1b5ad53920f47e8267add29cd09e59286a00c09203330d877f35a1c1a792657e8daa905eb9dd75e138ebea7e20c14230dd4489f0ac10ed98c794ee125792be5409f3c5a67c216d7cf3c1f0325184cfc8586aef5d6e4beec236c7f251e9fa8d1319f6d0ff95f01316383b669922d89247352a8dbbe5a0e8e95d881141389b9160117d3155c097ee4601d9ba9a04436aaaa01745d1bbc97cde05ca3aa241780bcc7bbff7a5402aa581c86e31405e3753e69670e887d099a26804c3dad8e8ebdad20f1461cb36d888a19c93494004ff60d74394c7de618c4044ba24f35df122503b7bc201509765e7c4f825a01f3db0ce7fe1edd9414b4469a584fd909a75ebbfbb3e333b398b09483e34b4790b31e0b1d23adcb69f5e1f70331e66412e45eadc1b04bd2176021e1f24b17e5ceb193e21fa4c3268bf047db28311def788cdaea4727e8a98a6a230c3cf67f54067e2a54a7517241bfbcc624987602a97847ef45017edf393e287e6a0752e8506326d44a16a17eff06968b1cdce5095b7ecdfebcb2dea67d1fbdbc536d12282bbc15bffa7ac1c1d50ffd320c938d26b8f1e6f7f325bc18d55f6ab9624189e4b794411e10d8aa3721a44d0cb08be09c8b9e99dad14a0d8f55001bd84d56ff767cd013c1d2d0f542d3bd696d80',
    'BITRIX_SM_SALE_UID': '526107829',
    '__cf_bm': 'sGdQaXeHZeCQS_LhP3C.wYFRRCp9ni2laWC6BGnJ9p8-1742300045-1.0.1.1-LTSTye2BXjrogmDug.ZqZvVTjQyYySpiSZhZZz2Iu_AkXMQ2E1NKXGNYrLy3QevtiGfmjBGyWJ_ddCiKjEiSj09hkUUS_Co67816kyetO_I',
    'cf_clearance': 'cMcTcGWjG1IIoitqRW.ELp2ajqrYGvm3WpWbUqTIyN4-1742299867-1.2.1.1-YcifYRlMYEpzodOraSGL2oWnQ0rsWvBSWymMe3MVuMFHiKkN_3N3TOzlhTFfwwJcrZZQA1amCs2Q8XhBxeEmWmfbppmltjtH949qGRJL.6lNIWH3ENWzVq_Bu_J1JjacfUmZAXblTzBxvCGrKakfvbXFXjcTWB0tvJkcHEIr80T0Klyk0bfYxpvvYgN7dd6GZBlKu666MAhQLZxZHZIl84E1yf424G0ac7wr3un9ENSXp63pw0IBMds2wbQp1ZXhRVlCRtC3XLTUfl6OeIChg6Wqw0Ku8J8S0C_fXbq3a8kWheaUg5hJhUCA1ZghpoAw0NkPzJJL1BcMcIPkxqoCuLUQaUBVdpT91zXUjBAREHc',
    'epic_digital_sid': '9340d1501af5b61ddce2481b4577f79d',
    'peasurement_protocol_vp': '1536x750',
    'peasurement_protocol_sr': '1536x864',
    'peasurement_protocol_sd': '24',
    'peasurement_protocol_de': 'UTF-8',
    'auth-status': 'out',
    'superUniqueId': '1028975a0842f98b6eda5cf4',
    'sc': '8575FA4D-D17D-CA22-D4B6-A8D8C62AE936',
    'CookieConsent': "{stamp:'-1',necessary:true,preferences:true,statistics:true,marketing:true,method:'implied',ver:1,utc:1742299870004,region:'UA'}",
    '_gcl_au': '1.1.1178697957.1742299870',
    '_ga': 'GA1.1.1571967268.1742299870',
    '_clck': 'd16wq7|2|fub|0|1903',
    'peasurement_protocol_ga12': 'GA1.1.1571967268.1742299870',
    '_fbp': 'fb.1.1742299873495.236607443916307690',
    'g_state': '{"i_l":0}',
    'load_site': 'yes',
    'hide_layout': '0',
    'auth._token.laravelSanctum': 'false',
    'auth._token_expiration.laravelSanctum': 'false',
    'XSRF-TOKEN': 'eyJpdiI6InY1SjFVeHBmVUlPbUM3cnB3azNJZ2c9PSIsInZhbHVlIjoiWGdzUWJtbGRBSXlKY2ptUjd6VWdtVDdtOXBuNTVTWDFVUWhTMis1b09mN2xidGZ6cTYyb0NvdlVjNklTUmNxSlwvYWhqV0wvSE1Pa2IxdzMzQXltdnRGdDk0dWNwRkpyOVgxT3hIZGRsUVF5bGVWUzhtVmJMc2RtYXViZlZZYlNQQkd3czY1b3dPZHl2bEFTNlgrckZsQTRvMTBOdHYwUHR5Z04tb0hnWUVBSjczN3dFa3FCZk5oZXRGc1ByOVhIQ2VJMjhhdDFNR0NvUHZrV1Z5ZFM0VnlcLmtjbw0iLCJtYWMiOiJlNDFmZTFiNzE0NmM4MTNkNzZlNzljZGY5Nzk5MzVjZDlhNjc0YTg1ZTgwZGJmMmEzYTgyZGFmYWMwM2Y1YWE4NTkxMzYzZGM4OGQ1MzU0MGY0ZDBmOTcwYjVjNzMwYjdiODk4ZDM1NzZiYzNhZTg5Mzc5OTMyYjk1NzA2ZDg0ZWQyZDBlY2F5RkN8PqY2ZGdUE9gLGKpZqH2U42oMbh1rqdbJGGVzxdrw=="'
}

def epicentr_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'class':'_aql9TB _7TBdaN _GuJjCI'}).text.strip()
        try:
            price_tag = soup.find('data', attrs={'itemprop':'price'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('s', attrs={'class': '_Yf4yHx'}).text.strip()
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
            image_tag = soup.find('img', attrs={'class': '_oAFqao'})
            image_url = image_tag['data-zoom']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        return product_name, price, old_price, discount, icon, image

if __name__ == "__main__":
    epicentr_price('https://epicentrk.ua/ua/shop/heimpad-bezdrotovyi-gamepro-gpx13t-2-4g-bt-5-1-usb-switch-pc-ios-android-rgb-transparent.html')
