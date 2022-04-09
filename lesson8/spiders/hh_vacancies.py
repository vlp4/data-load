import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from lesson8.items import VacancyItem, EmployerItem, extract_employer_id


class HhVacancySpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru', 'rabota.by']

    def __init__(self, search_params_string, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://balashov.hh.ru/search/vacancy{search_params_string}']

    def parse(self, response: HtmlResponse, **kwargs):
        vacancy_links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)

        page_links = response.xpath('//a[@data-qa="pager-page"]/@href').getall()
        for link in page_links:
            yield response.follow(link, callback=self.parse)

    def parse_vacancy(self, response: HtmlResponse):
        loader = ItemLoader(item=VacancyItem(), response=response)
        loader.add_value('source', self.name)
        loader.add_xpath('link', '//link[@rel="canonical"]/@href')
        loader.add_xpath('vacancy_id', '//input[@name="vacancyId"]/@value')
        loader.add_xpath('employer_id', '//a[@data-qa="vacancy-company-name"]/@href')
        loader.add_xpath('employer_title',
                         '//*[@data-qa="vacancy-company-name" or @class="vacancy-company-name"]//text()')
        loader.add_xpath('title', '//h1[@data-qa="vacancy-title"]/text()')
        loader.add_xpath('location', '//p[@data-qa="vacancy-view-location"]/text()')
        loader.add_xpath('compensation', '//div[@data-qa="vacancy-salary"]//text()')
        item = loader.load_item()

        company_link = response.xpath('//a[@data-qa="vacancy-company-name"]/@href').get()
        if company_link:
            yield response.follow(company_link, callback=self.parse_company,
                                  cb_kwargs={'employer_title': item.get('employer_title')})
        yield item

    def parse_company(self, response: HtmlResponse, **kwargs):
        loader = ItemLoader(item=EmployerItem(), response=response)

        # Need this for custom employer pages
        employer_title = kwargs.get('employer_title', None)
        if employer_title:
            loader.add_value('title', employer_title)
        else:
            loader.add_xpath('title', '//span[@data-qa="company-header-title-name"]/text()')

        loader.add_value('source', self.name)
        loader.add_xpath('link', '//link[@rel="canonical"]/@href')
        loader.add_value('employer_id', extract_employer_id(response.url))
        loader.add_xpath('business_area', '//div[@class="employer-sidebar-block"]//p/text()')
        loader.add_xpath('site', '//a[@data-qa="sidebar-company-site"]/@href')
        item = loader.load_item()
        yield item
