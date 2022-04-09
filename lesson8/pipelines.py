from lesson8.items import VacancyItem, EmployerItem
from lesson8.my_mongo import my_vacancies, my_employers


class SavePipeline:
    def process_item(self, item, spider):
        if isinstance(item, VacancyItem):
            collection = my_vacancies
            key = 'vacancy_id'
        elif isinstance(item, EmployerItem):
            collection = my_employers
            key = 'employer_id'
        else:
            raise Exception(f'Unsupported item type {item}')

        collection.update_one({'source': item['source'], key: item[key]}, update={'$set': item}, upsert=True)
        return item
