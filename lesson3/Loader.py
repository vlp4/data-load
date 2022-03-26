import abc
import re
import logging

import requests
from bs4 import BeautifulSoup as BS

log = logging.getLogger(__name__)


def parse_number(value):
    digits = re.sub(r'\D', '', value)
    return int(digits)


def parse_salary_value_and_currency(salary_element, expression):
    currency = None
    salary_min = None
    salary_max = None
    if salary_element:
        parts = re.search(expression, salary_element.text).groups()
        if len(parts) == 2:
            value = parts[0]
            currency = parts[1]
            dash = value.find('–')
            if dash > 0:
                salary_min = parse_number(value[:dash])
                salary_max = parse_number(value[dash + 1:])
            else:
                salary_max = parse_number(value)
    return salary_min, salary_max, currency


class Loader(metaclass=abc.ABCMeta):
    """Base class for loader implementations"""

    def __init__(self, search_value):
        self._next_page = 1
        self._search_value = search_value

    def load(self):
        log.info(f'Loading items from {self}')
        all_items = []
        while True:
            try:
                log.info(f'Loading page {self._next_page}...')
                page_items = self._load_page(self._next_page, self._search_value)
                self._next_page += 1
            except BaseException as err:
                log.warning(f'  Failed to load page {self._next_page}: {err}')
                page_items = []
            if len(page_items) < 1:
                log.info(f'  There are no more items, done.')
                break
            log.info(f'  Found {len(page_items)} items.')
            all_items.extend(page_items)
        log.info(f'  Loaded {len(all_items)} items total.')
        return all_items

    def _get_page_dom(self, url, params):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'}
        response = requests.get(url, params=params, headers=headers)
        dom = BS(response.text, 'html.parser')
        return dom

    @abc.abstractmethod
    def _load_page(self, page_1based, search_value):
        """Loads specified page using search value"""
        return []
