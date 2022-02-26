from Loader import Loader, parse_salary_value_and_currency


class LoaderHeadHunter(Loader):
    def _load_page(self, page_1based, search_value):
        items = []
        params = {
            'clusters': 'true',
            'area': '79',
            'ored_clusters': 'true',
            'enable_snippets': 'true',
            'text': search_value,
        }
        if page_1based > 1:
            params['page'] = page_1based - 1

        dom = self._get_page_dom(f'https://balashov.hh.ru/search/vacancy', params)
        vacancies = dom.select('.vacancy-serp .vacancy-serp-item')
        for vacancy in vacancies:
            compensation = vacancy.select_one('*[data-qa=vacancy-serp__vacancy-compensation]')
            salary_min, salary_max, currency = parse_salary_value_and_currency(compensation, r'^\D*(.+)\s(\w+)\.$')
            item = {
                'title': vacancy.select_one('.resume-search-item__name a').text,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': currency,
                'link': vacancy.select_one('.resume-search-item__name a').get('href'),
                'source': 'hh.ru'
            }
            items.append(item)

        return items
