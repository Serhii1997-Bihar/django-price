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

site_functions = {
                'allo': allo_price,
                'comfy': comfy_price,
                'epicentr': epicentr_price,
                'foxtrot': foxtrot_price,
                'rozetka': rozetka_price,
                'brain': brain_price,
                'makeup': makeup_price,
                'f': fua_price,
                'moyo': moyo_price,
                'citrus': citrus_price,
                'eva': eva_price,
                'intertop': intertop_price,
                'stylus': stylus_price,
                'yakaboo': yakaboo_price,
                'deka': deka_price,
                'bookye': bookye_price,
                'zara': zara_price,
                'eldorado': eldorado_price,
                'telemart': telemart_price,
                'osport': osport_price,
                'sinsay': sinsay_price,
                'reserved': reserved_price,
                'bi': bi_price
            }