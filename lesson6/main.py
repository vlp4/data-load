# II вариант
# 1) Создать пауков по сбору данных о книгах с сайтов labirint.ru и/или book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация должна складываться в базу данных

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.labirint import LabirintSpider
from spiders.book24 import Book24Spider

import settings

if __name__ == '__main__':
    my_settings = Settings()
    my_settings.setmodule(settings)

    process = CrawlerProcess(settings=my_settings)
    process.crawl(LabirintSpider)
    process.start()

    process = CrawlerProcess(settings=my_settings)
    process.crawl(Book24Spider)
    process.start()

