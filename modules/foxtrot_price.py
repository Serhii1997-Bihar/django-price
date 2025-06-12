import requests, re
from bs4 import BeautifulSoup
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(BASE_DIR, 'icons', 'foxtrot.png')

headers = {
    "alt-svc": 'h3=":443"; ma=86400',
    "cf-cache-status": 'DYNAMIC',
    "cf-ray": '9224c2d8eaf70b98-WAW',
    "content-encoding": 'br',
    "content-security-policy": "frame-ancestors 'self' youtube.googleapis.com www.youtube.com; default-src 'self' data: https:; manifest-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: gcdn.tranzzo.com youtube.googleapis.com www.foxtrot.com.ua wss://rtc-cloud-eu1.bitrix.info rtc-cloud-eu1.bitrix.info widget.eu.criteo.com www.google.com.ua *.google.com www.facebook.com paypartslimit.privatbank.ua *.google-analytics.com www.googleadservices.com www.googletagmanager.com socauth.privatbank.ua www.gstatic.com code.jquery.com cdn.jsdelivr.net connect.facebook.net esputnik.com static.criteo.net sslwidget.criteo.com script.softcube.com googleads.g.doubleclick.net maps.googleapis.com giftmall.com.ua bitrix.samsung.ua www.giveaway.foxtrot.com.ua cdn.admitad.com z.lenmit.com *.esputnik.com a4p.adpartner.pro a.mgid.com cm.mgid.com servereu.eyezon.online static.cloudflareinsights.com media.flixcar.com media.flixfacts.com logo.flixfacts.co.uk media.flixsyndication.net t.flix360.com syndication.flix360.com content.jwplatform.com assets-jpcust.jwpsrv.com ssl.p.jwpcdn.com *.cloudfront.net media.pointandplace.com player.pointandplace.com t.pointandplace.com *.flix360.com *.flix360.io dev-origin.flixsyndication.net dev-delivery.flix360.com measurement-api.criteo.com static.hotjar.com google-analytics.bi.owox.com script.hotjar.com api.tdl.com.ua ajax.googleapis.com static.hotjar.com wss://*.tokbox.com wss://*.opentok.com api.soc.business *.hotjar.com *.hotjar.io wss://*.hotjar.com *.tokbox.com *.opentok.com *.googlesyndication.com foxtrot-api.evinent.site *.foxtrot.com.ua widget-samsung.kwizbot.io tags.creativecdn.com ams.creativecdn.com push.esputnik.com region1.analytics.google.com *.kwizbot.io *.monolytics.app wss://*.monolytics.app *.newrelic.com *.nr-data.net foxtrot.com.ua;connect-src 'self' blob: widget.tranzzo.com youtube.googleapis.com www.foxtrot.com.ua wss://rtc-cloud-eu1.bitrix.info rtc-cloud-eu1.bitrix.info widget.eu.criteo.com www.google.com.ua *.google.com www.facebook.com paypartslimit.privatbank.ua api.foxtrot.evinent.site foxtrot-api.search.evinent.site tracker.softcube.com *.google-analytics.com sslwidget.criteo.com stats.g.doubleclick.net ai.softcube.com recom.softcube.com bitrix.samsung.ua giveaway.foxtrot.com.ua *.esputnik.com esputnik.com storage.googleapis.com servereu.eyezon.online wss://servereu.eyezon.online wss://wsseu.eyezon.online recordseu.eyezon.online cloudflareinsights.com *.google.com maps.googleapis.com wss://bitrix.samsung.ua media.flixcar.com media.flixfacts.com logo.flixfacts.co.uk media.flixsyndication.net t.flix360.com syndication.flix360.com content.jwplatform.com assets-jpcust.jwpsrv.com ssl.p.jwpcdn.com *.cloudfront.net media.pointandplace.com player.pointandplace.com t.pointandplace.com *.flix360.com *.flix360.io dev-origin.flixsyndication.net dev-delivery.flix360.com measurement-api.criteo.com static.hotjar.com google-analytics.bi.owox.com script.hotjar.com api.tdl.com.ua static.hotjar.com wss://*.tokbox.com wss://*.opentok.com *.hotjar.com *.hotjar.io wss://*.hotjar.com *.tokbox.com *.opentok.com api.soc.business *.googlesyndication.com foxtrot-api.evinent.site *.foxtrot.com.ua socket-samsung.kwizbot.io searchapi.samsung.com shop.samsung.com ams.creativecdn.com tags.creativecdn.com push.esputnik.com region1.analytics.google.com *.kwizbot.io wss://*.kwizbot.io api.ipify *.monolytics.app wss://*.monolytics.app *.newrelic.com *.nr-data.net foxtrot.com.ua; img-src * 'self' data: https: blob:; style-src 'self' 'unsafe-inline' blob: storage.googleapis.com www.foxtrot.com.ua i2.foxtrot.com.ua files.foxtrot.com.ua fonts.googleapis.com bitrix.samsung.ua macaroncms.s3.eu-central-1.amazonaws.com *.google.com media.flixcar.com media.flixfacts.com logo.flixfacts.co.uk media.flixsyndication.net t.flix360.com syndication.flix360.com content.jwplatform.com assets-jpcust.jwpsrv.com ssl.p.jwpcdn.com *.cloudfront.net media.pointandplace.com player.pointandplace.com t.pointandplace.com *.flix360.com *.flix360.io dev-origin.flixsyndication.net dev-delivery.flix360.com static.hotjar.com google-analytics.bi.owox.com api.tdl.com.ua wss://*.tokbox.com wss://*.opentok.com *.hotjar.com *.hotjar.io wss://*.hotjar.com *.tokbox.com *.opentok.com api.soc.business foxtrot-api.evinent.site widget-samsung.kwizbot.io push.esputnik.com *.kwizbot.io; font-src 'self' www.foxtrot.com.ua fonts.gstatic.com i2.foxtrot.com.ua storage.googleapis.com files.foxtrot.com.ua media.flixcar.com media.flixfacts.com logo.flixfacts.co.uk media.flixsyndication.net t.flix360.com syndication.flix360.com content.jwplatform.com assets-jpcust.jwpsrv.com ssl.p.jwpcdn.com *.cloudfront.net media.pointandplace.com player.pointandplace.com t.pointandplace.com *.flix360.com *.flix360.io dev-origin.flixsyndication.net dev-delivery.flix360.com *.kwizbot.io",
    "content-type": 'text/html; charset=utf-8',
    "date": 'Tue, 18 Mar 2025 12:33:54 GMT',
    "feature-policy": "accelerometer 'none'; camera 'self'; gyroscope 'none'; magnetometer 'none'; usb 'none'",
    "permissions-policy": "accelerometer=(), camera=(self), gyroscope=(), magnetometer=(), usb=()",
    "priority": 'u=0,i',
    "referrer-policy": 'no-referrer-when-downgrade',
    "server": 'cloudflare',
    "server-timing": 'cfExtPri',
    "strict-transport-security": 'max-age=31536000; includeSubDomains; preload',
    "vary": 'Accept-Encoding',
    "via": '1.1 b8f260e966cae470dbec70a43fd5e0ca.cloudfront.net (CloudFront)',
    "x-amz-cf-id": 'PTgAXJv-UBZjTY9Vw7hzSoiH2NgrlJ-irYzSIGNh0vzeEFPHSIrHSA==',
    "x-amz-cf-pop": 'FRA60-P10',
    "x-cache": 'Miss from cloudfront',
    "x-content-type-options": 'nosniff',
    "x-response-time-ms": '27',
    "x-xss-protection": '1; mode=block'
}
cookies = {
    "lang": "uk",
    "ft_city_id": "38044",
    "from_search": "",
    "_gcl_au": "1.1.436174791.1742301177",
    "sc": "C6E18AB9-C247-F67C-4838-D9BB417D3D66",
    "_ga": "GA1.1.545832725.1742301178",
    "FPID": "FPID2.3.4XwDPF%2Bq6BwanX78HAWFEKYAuuOmUuz4uiS7didcU5c%3D.1742301178",
    "FPLC": "ejzkXbLQEj04Zw3NHwfOkN07cgp8i%2FDNLr%2BcdMeeopmWo%2FLxSgPMupNQWsID%2BQOMaV86B1DJoI3euktf%2Bw5R5IyfglqSSHgdlI9rzpkl%2FUAmrMxxRRvgS5W%2Fm%2F%2F8yg%3D%3D",
    "FPGSID": "1.1742301179.1742301179.G-BMMPD020VE.S_X04cKPUdNVIVeBBqG5Vw",
    "monolytics-client-id": "67d967faf0fbd240710fdb5e",
    "monolytics-session-id": "67d967fa679acdc00fda76ee",
    "_fbp": "fb.2.1742301178939.812518024644653630",
    "cookie_chat_id": "704b0a84fa6b431c85e878e57534c07d",
    "slotToPDP_6990493": "Category%7C%7C%D0%9D%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA%D0%B8%7C%7CPopularity",
    "ft_recently": "_58%3A27110",
    "city-id": "38048",
    "__rtbh.lid": "%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22T5N8afdVbQatUotytsIX%22%2C%22expiryDate%22%3A%222026-03-18T12%3A33%3A33.652Z%22%7D",
    "__rtbh.uid": "%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-03-18T12%3A33%3A34.455Z%22%7D",
    "fp": "3",
    "lfp": "3/18/2025, 2:32:56 PM",
    "pa": "1742301177258.47440.9824981689906398www.foxtrot.com.ua0.2802899802066443+3",
    "positionToPDP_6990493": "",
    "_ga_BMMPD020VE": "GS1.1.1742301178.1.1.1742301215.0.0.949701636",
    "cto_bundle": "cS5Wyl91bExJTDlrZ0NFWk1JaUNFWFJkajlWTkE1YnV1JTJGSFBWMWRWUXl3dVpNYkdTd0pnQ3h3cWFjYVFwNVJ2dGxKcThYQXNUeDZOMWpJS2Z6RE9UVUZhUXhtSVNjY2l5MEVmaVh5WTg4WE8lMkJhSk9QYnJ6V2Y5b2F0anFhdkZLdnBEbnk3SEpnZHppbEk0UkMySmxlN3NJSHhBJTNEJTNE"
}

def foxtrot_price(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h1', attrs={'id':'product-page-title'}).text.strip()
        try:
            price_tag = soup.find('div', attrs={'class':'product-box__main_price'}).text.strip()
            price = re.sub(r'[^0-9.]', '', price_tag)
        except AttributeError:
            price = None

        try:
            old_tag = soup.find('div', attrs={'class': 'product-box__main_discount'}).find('label').text.strip()
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
            image_tag = soup.find('link', attrs={'rel': 'preload', 'as': 'image'})
            image_url = image_tag['href']
            if image_url:
                image_response = requests.get(image_url)
                image = image_response.content
        except AttributeError:
            image = None

        return product_name, price, old_price, discount, icon, image


if __name__ == "__main__":
    foxtrot_price('https://www.foxtrot.com.ua/uk/shop/televizoriy-bravis-32k5000h.html')