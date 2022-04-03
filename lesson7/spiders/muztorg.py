import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from lesson7.items import ProductItem


class MuztorgSpider(scrapy.Spider):
    name = 'muztorg'
    allowed_domains = ['muztorg.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.muztorg.ru/category/{search}']

    def parse(self, response: HtmlResponse, **kwargs):
        product_links = response.xpath('//div[@class="product-header"]//a/@href').getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath('//ul[@class="pagination"]/li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=ProductItem(), response=response)
        loader.add_value('source', self.name)
        loader.add_value('link', response.url)
        loader.add_xpath('item_id', '//section[@itemscope]//*[@itemprop="sku"]/@content')
        loader.add_xpath('title', '//section[@itemscope]//*[@itemprop="name"]/text()')
        loader.add_xpath('price', '//section[@itemscope]//*[@itemprop="price"]/@content')
        loader.add_xpath('photo_urls', '//section[@itemscope]'
                                       '//div[contains(@class, "product-gallery__slides")]//img/@data-src')
        item = loader.load_item()
        return item
