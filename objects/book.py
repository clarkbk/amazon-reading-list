import re

from client import client
from collections import OrderedDict
from pprint import pprint


class Book:
    def __init__(self, title, author):
        if ':' in title:
            self.title, self.subtitle = [t.strip() for t in title.split(':', 1)]
        else:
            self.title, self.subtitle = [title, '']
        self.author = author
        self.pub_year = None
        self.ben_score = None
        self.num_pages = None
        self.goodreads_num_ratings = None
        self.goodreads_avg_rating = None
        self.goodreads_url = ''
        self.goodreads_id = None
        self.asin = ''
        self.kindle_asin = ''
        self.isbn = None

    @property
    def short_title(self):
        return re.search(r'^([\w\s.]+)\:?', self.title).group(1).strip()

    def find_goodreads_id(self):
        def is_bogus(result):
            rtg = result['average_rating']
            rtg = float(rtg) if isinstance(rtg, str) else float(rtg['#text'])
            return (
                not isinstance(result, OrderedDict) or
                'summary' in result['best_book']['title'].lower() or
                'study guide' in result['best_book']['title'].lower() or
                int(result['ratings_count']['#text']) < 200 or
                rtg < 1.0
            )

        q = f'{self.author} {self.short_title}'
        try:
            results = client.search_book(q)
        except Exception as e:
            print(f'q="{q}"')
            pprint(client.search_book(q))
            raise e

        if ('results' not in results or results['results'] is None):
            return False
        results = results['results']['work']

        if not isinstance(results, list):
            results = [results]

        for result in results:
            if is_bogus(result):
                continue

            self.goodreads_id = int(result['best_book']['id']['#text'])
            return True

    def update_from_dict(self, d):
        for k, v in d.items():
            setattr(self, k, v)

    def update_from_goodreads_api(self):
        try:
            result = client.Book.show(self.goodreads_id)
        except Exception as e:
            pprint(self.__dict__)
            raise e

        keys_wanted = {
            'num_pages':        {'name': 'num_pages',               'type': int},
            'publication_year': {'name': 'pub_year',                'type': int},
            'isbn':             {'name': 'isbn',                    'type': str},
            'asin':             {'name': 'asin',                    'type': str},
            'kindle_asin':      {'name': 'kindle_asin',             'type': str},
            'link':             {'name': 'goodreads_url',           'type': str},
            'average_rating':   {'name': 'goodreads_avg_rating',    'type': float},
        }
        d = {}
        for k, v in result.items():
            if k not in keys_wanted.keys():
                continue
            if (v is None or v == 'None'):
                continue
            try:
                d[keys_wanted[k]['name']] = keys_wanted[k]['type'](v)
            except TypeError as e:
                pprint({k, v})
                pprint(keys_wanted[k])
                raise e

        d['goodreads_num_ratings'] = int(result['work']['ratings_count']['#text'])

        self.update_from_dict(d)
