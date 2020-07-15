import os

import pytest

from hackernews.exceptions import ParseError
from hackernews.parsers import parse_topstories


def test_parse_topstories_bad_response(requests_mock):
    requests_mock.get('https://news.ycombinator.com/', text='text')
    with pytest.raises(ParseError):
        parse_topstories()


def test_parse_topstories_empty_posts(requests_mock):
    requests_mock.get('https://news.ycombinator.com/', text='</html>')
    with pytest.raises(ParseError):
        parse_topstories()


def test_parse_topstories(requests_mock):
    path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'fixtures', 'hackernews.html')
    with open(path, 'r') as fh:
        requests_mock.get('https://news.ycombinator.com/', text=fh.read())

    posts = parse_topstories()

    assert len(posts) == 30

    # first post
    assert '23842179' in posts.keys()
    assert 'https://element.io/blog/welcome-to-element/' == posts['23842179']['url']
    assert 'Riot is now Element' == posts['23842179']['title']
    # last post
    assert '23834153' in posts.keys()
    assert 'https://jordanlewis.org/posts/twitch-live-coding/' == posts['23834153']['url']
    assert 'How to Run a Live Coding Stream on Twitch Using OBS' == posts['23834153']['title']
