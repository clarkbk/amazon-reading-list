## Installation

```
$ mkvirtualenv amazon-reading-list
$ workon amazon-reading-list
$ pip install -r requirements.txt
```

## Configuration

Set up `.env` file:

```
$ cp .env.sample .env
# edit GOODREADS_API_KEY
```

Get wishlist HTML

1. go to wishlist page on amazon
1. scroll to bottom til lazyloading is complete
1. inspect element
1. find `ul#g-items` element
1. right-click, copy element
1. paste into `input/amazon-wishlist.html`

Get content library list HTML

1. go to content library page on amazon
1. inspect element
1. find parent `ul` element
1. right-click, copy element
1. paste into `input/amazon-content-library.html`

## Use

```
$ python3 run.py
```
