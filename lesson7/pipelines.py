import re

import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline

from items import ProductItem


def clean_path(s: str):
    s2 = re.sub('[^a-z_0-9]', '', s.lower())
    if len(s2) < 1:
        s2 = 'unknown'
    return s2


class SavePhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item: ProductItem, info):
        if 'photo_urls' in item:
            url_set = {url: True for url in item['photo_urls']}
            for img in url_set.keys():
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item: ProductItem, info):
        item['photo_files'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item: ProductItem = None):
        path = super().file_path(request, response, info, item=item)
        path2 = f'{clean_path(item["item_id"])}/{path}'
        return path2


class SaveProductPipeline:
    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['geek-course']
        self.collection = db.products
        self.collection.create_index([("source", 1), ("item_id", 1)], unique=True)

    def process_item(self, item: ProductItem, spider):
        self.collection.update_one({
            'source': item['source'],
            'item_id': item['item_id']
        }, update={'$set': item}, upsert=True)
        return item
