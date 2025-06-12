import os
import sys

import django

sys.path.append("/")
os.environ["DJANGO_SETTINGS_MODULE"] = "pricesua_project.settings"
django.setup()