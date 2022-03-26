import scrapy
from scrapy.http import HtmlResponse

from lesson6.items import BookItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.css('a.product-card__image-link.smartLink').xpath('./@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_book)

        if links:
            page = kwargs.get('page', 1)
            url = kwargs.get('url', response.url)
            next_link = f'{url}page-{page+1}/'
            yield response.follow(next_link, callback=self.parse, cb_kwargs={'url': url, 'page': page+1})

    def parse_book(self, response: HtmlResponse):
        info = response.xpath('//div[@class="product-detail-page__body"]')
        title = info.xpath('.//div[@class="product-detail-page__title-holder"]/h1/text()').get().strip()
        author = info.xpath('.//span[@itemprop="author"]/meta/@content').get()
        rating = float(response.xpath('.//span[@class="rating-widget__main-text"]/text()').get().replace(',', '.'))
        price = float(info.xpath('.//meta[@itemprop="price"]/@content').get())
        category = info.xpath('.//meta[@itemprop="genre"]/@content').get()
        return BookItem(
            source='book24',
            item_id=response.url,
            title=title,
            link=response.url,
            author=author,
            price=price,
            category=category,
            rating=rating,
        )
