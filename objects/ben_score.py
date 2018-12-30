class BenScore:
    EXPONENTS = {
        'rating':   2.2,
        'reviews': 1/52,
        'pages':  1/6.3,
    }
    WEIGHTS = {
        'rating':   0.6,
        'reviews':  0.3,
        'pages':    0.1,
    }
    RATING_SCALE = 5.0

    def __init__(self, book):
        self.book = book
        book.ben_score = self

        self.mod_rating_score = self.book.goodreads_avg_rating ** \
            (__class__.EXPONENTS['rating'])
        self.mod_reviews_score = self.book.goodreads_num_ratings ** \
            (__class__.EXPONENTS['reviews'])
        self.mod_pages_score = (1500 - self.book.num_pages) ** \
            (__class__.EXPONENTS['pages']) if self.book.num_pages else None

    def normalize(self, max_rating_score, max_reviews_score, max_pages_score):
        self.norm_rating_score = self.mod_rating_score / max_rating_score * \
            (__class__.RATING_SCALE)
        self.norm_reviews_score = self.mod_reviews_score / max_reviews_score * \
            (__class__.RATING_SCALE)
        self.norm_pages_score = self.mod_pages_score / max_pages_score * \
            (__class__.RATING_SCALE) if self.mod_pages_score else None

    @property
    def score(self):
        norm_scores = [
            self.norm_rating_score,
            self.norm_reviews_score,
            self.norm_pages_score,
        ]
        weights = list(__class__.WEIGHTS.values())
        score = 0
        if self.book.num_pages is not None:
            score = sum([a * b for a, b in zip(norm_scores, weights)])
            score /= sum(weights)
        else:
            score = sum([a * b for a, b in zip(norm_scores[:2], weights[:2])])
            score /= sum(weights[:2])
        return score

    def __str__(self):
        return str(round(self.score, 3))
