import re
import sys

import requests

from . import logger


def parse_topstories():
    """
    It's better to parse the API (https://github.com/HackerNews/API),
    but there are too many requests (1 + posts_count).
    """

    try:
        r = requests.get('https://news.ycombinator.com/')
    except requests.RequestException as e:
        logger.error('Page load failed')
        raise

    # page is fully loaded?
    if '</html>' not in r.text:
        logger.error('Page not fully loaded')
        sys.exit(1)

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
            logger.error('Parse post data failed', post_match)
            sys.exit(1)

        result.update({
            post_match.group('id'): {
                'post_id': post_match.group('id'),
                'url': post_data.group('url'),
                'title': post_data.group('title')
            }
        })

    if not result:
        logger.error('Posts empty')
        sys.exit(1)

    return result
