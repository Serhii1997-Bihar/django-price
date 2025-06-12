import os
import sys
import django
from urllib.parse import urlparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricesua_project.settings")
django.setup()

from prices_app.models import ProductModel, PriceModel
from modules.allo_price import allo_price
from modules.comfy_price import comfy_price
from modules.epicentr_price import epicentr_price
from modules.foxtrot_price import foxtrot_price
from modules.makeup_price import makeup_price
from modules.eva_price import eva_price
from modules.stylus_price import stylus_price
from modules.rozetka_price import rozetka_price
from modules.eldorado_price import eldorado_price
from modules.intertop_price import intertop_price
from modules.citrus_price import citrus_price
from modules.yakaboo_price import yakaboo_price
from modules.reserved_price import reserved_price
from modules.sinsay_price import sinsay_price
from modules.bi_price import bi_price
from modules.moyo_price import moyo_price
from modules.telemart_price import telemart_price
from modules.fua_price import fua_price
from modules.zara_price import zara_price
from modules.bookye_price import bookye_price
from modules.osport_price import osport_price
from modules.deka_price import deka_price
from modules.brain_price import brain_price
from urllib.parse import urlparse

SCRAPER_MAP = {
    'brain.com.ua': brain_price,
    'allo.ua': allo_price,
    'ctrs.com.ua': citrus_price,
    'comfy.ua': comfy_price,
    'epicentrk.ua': epicentr_price,
    'eva.ua': eva_price,
    'foxtrot.com.ua': foxtrot_price,
    'f.ua': fua_price,
    'intertop.ua': intertop_price,
    'makeup.com.ua': makeup_price,
    'moyo.ua': moyo_price,
    'rozetka.com.ua': rozetka_price,
    'stylus.ua': stylus_price,
    'yakaboo.ua': yakaboo_price,
    'book-ye.com.ua': bookye_price,
    'zara.com': zara_price,
    'eldorado.ua': eldorado_price,
    'telemart.ua': telemart_price,
    'osport.ua': osport_price,
    'sinsay.com': sinsay_price,
    'reserved.com': reserved_price,
    'deka.ua': deka_price,
    'bi.ua': bi_price
}


def normal_domain(link):
    domain = urlparse(link).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def get_scraper(link):
    domain = normal_domain(link)
    return SCRAPER_MAP.get(domain)

def add_prices():
    products = ProductModel.objects.all()

    for product in products:
        scraper_func = get_scraper(product.link)
        if scraper_func is None:
            print(f"Script not founded: {product.link}")
            continue

        try:
            result = scraper_func(product.link)
            if not result:
                print(f"Not founded - {product.link}")
                continue

            product_name, price, old_price, discount, icon, image = result

            PriceModel.objects.create(
                product=product,
                price=price,
                old_price=old_price,
                discount=discount
            )

            print(f"{product.product_name} added new price!")

        except Exception as e:
            print(f"Error with {product.link}: {e}")


if __name__ == "__main__":
    add_prices()
