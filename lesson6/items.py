import scrapy


class BookItem(scrapy.Item):
    source = scrapy.Field()
    item_id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    rating = scrapy.Field()

