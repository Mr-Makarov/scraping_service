import asyncio
import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parser import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parser = (
    (work_on_hh, "work_on_hh")
    )


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q["city_id"], q["language_id"]) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q["city_id"], q["language_id"]): q["url_data"] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='moskva').first()
# language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
func, key = parser

for data in url_list:
    url = data['url_data'][key]
    jobs, errors = func(url, city=data['city'], language=data['language'])

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.text', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()

