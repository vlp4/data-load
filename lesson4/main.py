# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для
# парсинга использовать XPath. Структура данных должна содержать:
# * название источника;
# * наименование новости;
# * ссылку на новость;
# * дата публикации.

# 2. Сложить собранные новости в БД
# Минимум один сайт, максимум - все три

import logging
import pandas as pd
from pprint import pprint

import pymongo

from Loader import Loader

logging.basicConfig(level=logging.INFO)
pd.options.display.width = 0

log = logging.getLogger(__name__)

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['geek-course']
collection = db.news
collection.create_index([("link", 1)], unique=True)

RSS_PATHS = {
    'items': '//item',
    'title': './/title/text()',
    'link': './/link/text()',
    'date': './/pubDate/text()'
}


def save_item(item):
    collection.update_one({'link': item['link']}, update={'$set': item}, upsert=True)


def load_news():
    all_items = []
    for loader in [
        Loader(True, 'mail.ru', 'https://news.mail.ru/rss/main/', RSS_PATHS),
        Loader(True, 'lenta.ru', 'https://lenta.ru/rss', RSS_PATHS),
        Loader(False, 'yandex news', 'https://yandex.ru/news/', {
            'items': '//div[contains(@class, "mg-grid__item")]',
            'title': './/h2/a/text()',
            'link': './/h2/a/@href',
            'date': './/span[@class="mg-card-source__time"]/text()'
        })
    ]:
        items = loader.load()
        all_items += items

    for item in all_items:
        save_item(item)
    return all_items


load_news()

saved = collection.find({})
pprint(list(saved))
