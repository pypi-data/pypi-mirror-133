#!/usr/bin/env python
import urllib
from typing import Dict, List, Optional, Set, Tuple, Union

import codefast as cf
from bs4 import BeautifulSoup

from rss.urlparser import TextBody, UrlParser


class TensorFlowBlog(UrlParser):
    """ A parser for fetching blog links from the TensorFlow website: https://blog.tensorflow.org/
    """
    def __init__(self, url: str, host: str) -> None:
        super().__init__(url, host)

    def parse(self, soup: BeautifulSoup):
        """Return a list of tuples, each tuple contains a url and a title.
        Each div contains a link to a blog post, a date, and a tag, as shown below:
        """
        for link in soup.find_all('div', class_='tensorsite-card'):
            blog = {
                'url':
                link.find('a').get('href'),
                'title':
                link.find('div',
                          class_='tensorsite-content__title').text.strip(),
                'date':
                link.find('span',
                          class_='tensorsite-content__info').text.strip()
            }
            blog = TextBody(**blog)
            self.results[blog.url] = blog
        return self.results
