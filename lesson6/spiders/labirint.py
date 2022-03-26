import scrapy
from scrapy.http import HtmlResponse

from lesson6.items import BookItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.css('.product a.cover').xpath('./@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_book)

        next_link = response.css('.pagination-number-viewport a').attrib.get('href')
        if next_link:
            yield response.follow(next_link, callback=self.parse)
        pass

    def parse_book(self, response: HtmlResponse):
        info = response.css('#product-info')
        author = ', '.join(info.xpath('.//*[@class="authors"]/a/text()').getall())
        rating = float(response.xpath('.//*[@id="rate"]/text()').get())
        attrib = info.attrib
        book_id = attrib.get('data-product-id')
        title = attrib.get('data-name')
        price_discount = float(attrib.get('data-discount-price'))
        price = float(attrib.get('data-price'))
        category = attrib.get('data-maingenre-name')
        return BookItem(
            source='labirint',
            item_id=book_id,
            title=title,
            link=response.url,
            author=author,
            price_discount=price_discount,
            price=price,
            category=category,
            rating=rating,
        )
