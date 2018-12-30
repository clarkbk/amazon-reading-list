import logging
import re
from tqdm import tqdm

from bs4 import BeautifulSoup
from objects.book import Book
from objects.reading_list import ReadingList


logger = logging.getLogger('app')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger.info(f'Starting...')

dict_list = []

with open('input/amazon-content-library.html', 'rb') as f:
    soup = BeautifulSoup(f, 'html.parser')

items = soup.find_all('li')
logger.info(f'Got {len(items)} books from Amazon owned content library.')
for item in items:
    d = {
        'title': item.find('div', id=re.compile(r'title\d+')).text,
        'author': item.find('div', id=re.compile(r'author\d+')).text,
    }
    dict_list.append(d)

with open('input/amazon-wishlist.html', 'rb') as f:
    soup = BeautifulSoup(f, 'html.parser')

items = soup.find_all('li', class_='g-item-sortable')
logger.info(f'Got {len(items)} books from Amazon wishlist.')
for item in items:
    byline = item.find('span', id=re.compile('^item-byline')).text
    author = re.search(r'^by\s([\w\s.]+)[,(]', byline)
    d = {
        'title': item.find('a', id=re.compile('^itemName_')).text,
        'author': str.replace(author.group(1), '.', '').strip(),
    }
    dict_list.append(d)

logger.info(f'Getting book metadata...')
r = ReadingList()
with tqdm(total=len(dict_list)) as pbar:
    for item in dict_list:
        pbar.update(1)

        book = Book(**item)
        found = book.find_goodreads_id()
        if not found:
            continue
        book.update_from_goodreads_api()
        r.add_book(book)

logger.info(f'Calculating Ben scores...')
r.calculate_ben_scores()
r.sort()

logger.info(f'Writing to CSV...')
r.csv_export('output/readinglist.csv')
logger.info(f'Done!')
