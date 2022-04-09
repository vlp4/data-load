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

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings

from spiders.labirint import LabirintSpider
from spiders.book24 import Book24Spider

import settings

if __name__ == '__main__':
    my_settings = Settings()
    my_settings.setmodule(settings)

    runner = CrawlerRunner(my_settings)
    runner.crawl(LabirintSpider)
    runner.crawl(Book24Spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
