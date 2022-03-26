import pymongo

from items import BookItem


class BooksPipeline:

    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['geek-course']
        self.collection = db.books
        self.collection.create_index([("source", 1), ("item_id", 1)], unique=True)

    def process_item(self, item: BookItem, spider):
        self.collection.update_one({
            'source': item['source'],
            'item_id': item['item_id']
        }, update={'$set': item}, upsert=True)
        return item