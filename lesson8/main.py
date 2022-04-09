# Творческое задание:
# 1. Выбрать любой источник открытых данных
# 2. Собрать данные в базу Mongo
# 3. Провести извлечение полученных данных

# Реализация сбора вакансий и работодателей из HH

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from lesson8.my_mongo import my_vacancies, my_employers
from spiders.hh_vacancies import HhVacancySpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhVacancySpider, search_params_string="?schedule=remote")
    # process.start()

    print('Vacancy count:', my_vacancies.count_documents({}))
    print('Employer count:', my_employers.count_documents({}))

