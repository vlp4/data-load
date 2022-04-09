import re
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join


def parse_float(value):
    value = value.replace('\xa0', '')
    try:
        return float(value)
    except:
        return value


def parse_number(value):
    digits = re.sub(r'\D', '', value)
    return int(digits)


def extract_employer_id(value):
    match = re.search(r'/employer/(\d+)', value)
    the_id = match.group(1) if match.groups() else None
    return the_id


class EmployerItem(scrapy.Item):
    source = scrapy.Field(output_processor=TakeFirst())
    employer_id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    business_area = scrapy.Field(output_processor=TakeFirst())
    site = scrapy.Field(output_processor=TakeFirst())


class VacancyItem(scrapy.Item):
    source = scrapy.Field(output_processor=TakeFirst())
    vacancy_id = scrapy.Field(output_processor=TakeFirst())
    employer_id = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(extract_employer_id))
    employer_title = scrapy.Field(output_processor=Join())
    title = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    compensation = scrapy.Field(output_processor=Join())
    location = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    skills_required = scrapy.Field(output_processor=TakeFirst())

