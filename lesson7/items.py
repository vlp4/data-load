import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def parse_float(value):
    value = value.replace('\xa0', '')
    try:
        return float(value)
    except:
        return value


class ProductItem(scrapy.Item):
    source = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    item_id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(parse_float))
    photo_urls = scrapy.Field()
    photo_files = scrapy.Field()

