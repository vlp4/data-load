# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
# должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц
# сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
#
# * Наименование вакансии.
# * Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# * Ссылку на саму вакансию.
# * Сайт, откуда собрана вакансия.

# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в
# json либо csv.

import logging
import pandas as pd

from LoaderHeadHunter import LoaderHeadHunter
from LoaderSuperJob import LoaderSuperJob


logging.basicConfig(level=logging.INFO)
pd.options.display.width = 0

search = 'python'

all_items = []
for loader in [
        LoaderHeadHunter(search),
        LoaderSuperJob(search),
    ]:
    items = loader.load()
    all_items += items

df = pd.DataFrame(all_items)
print(df)

df.to_csv('out/vacancies.csv')
