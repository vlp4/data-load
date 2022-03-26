import logging
from datetime import datetime

import requests
from lxml import html, etree

log = logging.getLogger(__name__)


def clean(val):
    if isinstance(val, list):
        val = val[0] if len(val) > 0 else None
    val = val.replace('\xa0', ' ')
    return val


class Loader:
    """Base class for loader implementations"""

    def __init__(self, is_xml, source_name, url, field_paths):
        self._is_xml = is_xml
        self._source_name = source_name
        self._url = url
        self._field_paths = field_paths

    def load(self):
        log.info(f'Loading items from {self}')
        items = []
        try:
            paths = self._field_paths.copy()
            items_xpath = paths['items']
            paths.pop('items', None)
            doc = self._load_document(self._url)
            elements = doc.xpath(items_xpath)
            for element in elements:
                item = {
                    'source': self._source_name
                }
                for property_name, xpath in paths.items():
                    value = clean(element.xpath(xpath))
                    item[property_name] = value

                if len(item['date']) < 6:  # Replace time-only value with current date
                    item['date'] = datetime.now().strftime('%d.%m.%Y')

                items.append(item)
                print(f'Item loaded {item}')
        except BaseException as err:
            log.warning(f'  Failed to load: {err}')
        log.info(f'  Found {len(items)} items.')
        return items

    def _load_document(self, url, params={}):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0'}
        response = requests.get(url, params=params, headers=headers)
        dom = etree.fromstring(response.content) if self._is_xml else html.fromstring(response.content)
        return dom