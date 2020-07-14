import re

import requests

from . import logger
from .exceptions import ParseError


def parse_topstories():
    """
    It's better to parse the API (https://github.com/HackerNews/API),
    but there are too many requests (1 + posts_count).
    """

    try:
        r = requests.get('https://news.ycombinator.com/')
    except requests.RequestException as e:
        raise ParseError('Page load failed', e)

    # page is fully loaded?
    if '</html>' not in r.text:
        raise ParseError('Page not fully loaded')

    RE_POSTS = re.compile(
        r'<tr[^>]+id=[\'"]{0,1}(?P<id>\d+)[\'"]{0,1}[^>]>' + \
        r'(?P<body>[\w\W]+?)'+ \
        r'</tr>'
    )
    RE_POST_DATA = re.compile(
        r'<a[^>]+href=["\']{1}(?P<url>[^"\']+)["\']{1}[^>]+' + \
        r'storylink["\']{1}[^>]*>' + \
        r'(?P<title>[^<]+)' + \
        r'</a>'
    )

    result = dict()

    for post_match in RE_POSTS.finditer(r.text):
        post_data = RE_POST_DATA.search(post_match.group('body'))
        if not post_data:
            raise ParseError('Parse post data failed', post_match)

        result.update({
            post_match.group('id'): {
                'post_id': post_match.group('id'),
                'url': post_data.group('url'),
                'title': post_data.group('title')
            }
        })

    if not result:
        raise ParseError('Posts empty')

    return result
