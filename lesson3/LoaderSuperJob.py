from Loader import Loader, parse_salary_value_and_currency


class LoaderSuperJob(Loader):
    def _load_page(self, page_1based, search_value):
        items = []
        base_url = 'https://saratov.superjob.ru'
        dom = self._get_page_dom(f'{base_url}/vacancy/search/', {
            'keywords': 'python',
            'page': page_1based
        })
        vacancies = dom.select('.f-test-search-result-item:has(a)')
        for vacancy in vacancies:
            compensation = vacancy.select_one('.f-test-text-company-item-salary')
            salary_min, salary_max, currency = parse_salary_value_and_currency(compensation, r'^\D*(.+)\s(\w+)\./\w+$')
            link = vacancy.select_one('a')
            title = link.text
            href = link.get('href')
            if href.find('://') < 0:
                href = base_url + href

            if len(title) > 0:
                item = {
                    'title': title,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'salary_currency': currency,
                    'link': href,
                    'source': 'superjob.ru'
                }
                items.append(item)

        return items
