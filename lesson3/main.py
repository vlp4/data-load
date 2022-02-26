# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет
# добавлять только новые вакансии/продукты в вашу базу.

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой
# суммы (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос
# для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна,
# а запрос проверяет оба поля)

import sys
import logging
import pandas as pd
from pprint import  pprint

import pymongo

from LoaderHeadHunter import LoaderHeadHunter
from LoaderSuperJob import LoaderSuperJob


logging.basicConfig(level=logging.INFO)
pd.options.display.width = 0

log = logging.getLogger(__name__)

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['geek-course']
collection = db.vacancies
collection.create_index([("link", 1)], unique=True)


def save_vacancy(item):
    collection.update_one({'link': item['link']}, update={'$set': item}, upsert=True)


def find_vacancies(min_salary):
    found = collection.find({'$or': [
        {'salary_min': {'$gt': min_salary}},
        {'salary_max': {'$gt': min_salary}}
    ]})
    return list(found)


def load_vacancies(search):
    all_items = []
    for loader in [
            LoaderHeadHunter(search),
            LoaderSuperJob(search),
        ]:
        items = loader.load()
        all_items += items

    for item in all_items:
        save_vacancy(item)
    return all_items


if len(sys.argv) < 2:
    log.info('Loading vacancies...')
    load_vacancies('python')
else:
    min_salary = int(sys.argv[1])
    log.info(f'Selecting vacancies with salary from {min_salary}')
    found = find_vacancies(min_salary)
    log.info(f'Found {len(found)} vacancies:')
    pprint(found)
