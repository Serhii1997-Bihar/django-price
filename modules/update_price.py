import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricesua_project.settings")

import django
django.setup()

from django.core.mail import send_mail
from prices_app.models import PersonModel
from django.shortcuts import get_object_or_404
import pricesua_project.settings
from modules.telegram_send import send_message

from prices_app.models import ProductModel, PriceModel
from modules.allo_price import allo_price
from modules.comfy_price import comfy_price
from modules.epicentr_price import epicentr_price
from modules.foxtrot_price import foxtrot_price
from modules.makeup_price import makeup_price
from modules.stylus_price import stylus_price
from modules.laluna_price import laluna_price
from modules.eldorado_price import eldorado_price
from modules.intertop_price import intertop_price
from modules.citrus_price import citrus_price
from modules.yakaboo_price import yakaboo_price
from modules.reserved_price import reserved_price
from modules.estro_price import estro_price
from modules.moyo_price import moyo_price
from modules.fua_price import fua_price
from modules.answear_price import answear_price
from modules.deka_price import deka_price
from modules.brain_price import brain_price
from modules.prom_price import prom_price
from modules.kasta_price import kasta_price
from modules.women_price import women_price
from modules.ager_price import ager_price
from modules.issa_price import issa_price
from modules.ridit_price import ridit_price
from modules.shafa_price import shafa_price
from urllib.parse import urlparse

SCRAPER_MAP = {
    'brain.com.ua': brain_price,
    'allo.ua': allo_price,
    'ctrs.com.ua': citrus_price,
    'comfy.ua': comfy_price,
    'epicentrk.ua': epicentr_price,
    'foxtrot.com.ua': foxtrot_price,
    'f.ua': fua_price,
    'intertop.ua': intertop_price,
    'makeup.com.ua': makeup_price,
    'moyo.ua': moyo_price,
    'laluna.com.ua': laluna_price,
    'stls.store': stylus_price,
    'yakaboo.ua': yakaboo_price,
    'eldorado.ua': eldorado_price,
    'answear.ua': answear_price,
    'reserved.com': reserved_price,
    'deka.ua': deka_price,
    'estro.ua': estro_price,
    'prom.ua': prom_price,
    'kasta.ua': kasta_price,
    'mo-woman.com.ua': women_price,
    'ager.ua': ager_price,
    'ridit.com.ua': ridit_price,
    'issaplus.com': issa_price,
    'shafa.ua': shafa_price
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

            last_price = PriceModel.objects.filter(product=product).order_by('-id').first()

            from decimal import Decimal

            price_decimal = Decimal(str(price))
            last_price_decimal = last_price.price

            if last_price and last_price_decimal == price_decimal:
                print(f"Ціна на {product.product_name} без змін. Пропускаємо.")
                print("-" * 120)
                continue

            PriceModel.objects.create(
                product=product,
                price=price,
                old_price=old_price,
                discount=discount)

            for user in product.users.all():
                person = get_object_or_404(PersonModel, user=user)

                old_price_str = f"{old_price} UAH" if old_price else "-"
                discount_str = f"{discount}%" if discount else "-"

                caption = (
                    f"🔗 {product.link}\n"
                    f"📦 {product_name}\n"
                    f"💰 Ціна: {price} UAH\n"
                    f"🔻 Попередня: {old_price_str}\n"
                    f"🎯 Знижка: {discount_str}"
                )

                chat_id = person.chat_id
                if chat_id:
                    send_message(chat_id, image, caption)
                else:
                    print("Відсутній ID чату.")

                send_mail(
                    subject=f"Discount information",
                    message=caption,
                    from_email=pricesua_project.settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False)

            print(f"Ціна на {product.product_name} змінилась. Даємо нову ціну.")
            print("-" * 120)

        except Exception as e:
            print(f"Помилка {product.link}: {e}")


if __name__ == "__main__":
    add_prices()
