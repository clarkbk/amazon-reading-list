import csv

from objects.ben_score import BenScore
from objects.book import Book


class ReadingList:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def csv_export(self, outfile):
        fieldnames = vars(Book('', '')).keys()
        with open(outfile, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([b.__dict__ for b in self.books])

    def calculate_ben_scores(self):
        max_rating, max_pages, max_reviews = -1, -1, -1
        for b in self.books:
            bs = BenScore(b)

            max_rating = max(bs.mod_rating_score, max_rating)
            max_reviews = max(bs.mod_reviews_score, max_reviews)
            if bs.mod_pages_score is not None:
                max_pages = max(bs.mod_pages_score, max_pages)

        for b in self.books:
            b.ben_score.normalize(max_rating, max_reviews, max_pages)

        return

    def sort(self, ben_score_desc=True):
        self.books.sort(key=lambda b: b.ben_score.score, reverse=ben_score_desc)
