import pymongo

my_client = pymongo.MongoClient('127.0.0.1', 27017)
my_db = my_client['geek-course']
my_vacancies = my_db.vacancies
my_employers = my_db.employers
my_vacancies.create_index([("source", 1), ("vacancy_id", 1)], unique=True)
my_employers.create_index([("source", 1), ("employer_id", 1)], unique=True)