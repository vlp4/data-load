# 1) Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
# ● название;
# ● все фото;
# ● ссылка;
# ● цена.
# Реализуйте очистку и преобразование данных с помощью ItemLoader.
# Цены должны быть в виде числового значения.
#
# Дополнительно:
# 2)Написать универсальный обработчик характеристик товаров, который будет формировать
# данные вне зависимости от их типа и количества.
# 3)Реализовать хранение скачиваемых файлов в отдельных папках,
# каждая из которых должна соответствовать собираемому товару

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.muztorg import MuztorgSpider
import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(MuztorgSpider, search="akusticheskie-udarnye")
    process.start()
