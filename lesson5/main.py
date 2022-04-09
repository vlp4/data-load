# Вариант II
#
# 2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД. Сайт
# можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
from pprint import pprint

from MVideoLoader import MVideoLoader

options = Options()
options.add_argument('--window-size=1200,900')
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

goods = MVideoLoader().load_goods(driver)
driver.quit()

pprint(goods)

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['geek-course']
collection = db.goods
collection.create_index([("link", 1)], unique=True)

for item in goods:
    collection.update_one({'link': item['link']}, update={'$set': item}, upsert=True)

