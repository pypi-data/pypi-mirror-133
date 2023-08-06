#!/usr/bin/env python
import codefast as cf
from typing import List, Dict, Tuple, Set, Optional, Union
from bs4 import BeautifulSoup
import urllib
from rss.urlparser import UrlParser, TextBody

class OpenAI(UrlParser):
    """ A parser for fetching blog links from the OpenAI website: https://openai.com/blog/
    """
    def __init__(self, url: str, host: str) -> None:
        super().__init__(url, host)

    def parse(self, soup: BeautifulSoup):
        """Return a list of tuples, each tuple contains a url and a title.
        Each div contains a link to a blog post, a date, and a tag, as shown below:
        [   
            <a href="/blog/improving-factual-accuracy/">WebGPT: Improving the factual accuracy of language models through web browsing</a>, 
            <a class="color-fg-50" href="/blog/improving-factual-accuracy/"> <time datetime="2021-12-16">December 16, 2021</time> </a>, 
            <a href="/blog/tags/research/">Research</a>
        ]
        """
        for link in soup.find_all('div', class_='post-card-full'):
            blog = {}
            for i, a in enumerate(link.find_all('a')):
                if i == 0:
                    blog['url'] = urllib.parse.urljoin(self.host,
                                                       a.get('href'))
                    blog['title'] = a.text
                elif i == 1:
                    blog['date'] = a.text.strip()
                elif i == 2:
                    blog['tag'] = a.text
            blog = TextBody(**blog)
            self.results[blog.url] = blog
        return self.results
