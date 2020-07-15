import pytest

from hackernews.models import Post
from hackernews.exceptions import HTTPBadRequestJSON
from hackernews.validators import (validate_int, validate_order_field,
                                   validate_order_type)


def test_validate_int():
    assert validate_int(10, 'text') == 10
    assert validate_int(1000, 'text') == 1000
    assert validate_int(1000, 'text', 15) == 15
    assert validate_int(-10, 'text', disallow_zero=False) == 0
    with pytest.raises(HTTPBadRequestJSON):
        validate_int(-10, 'text', disallow_zero=True)
        validate_int('--1', 'text', disallow_zero=True)
        validate_int('abc', 'text', disallow_zero=True)


def test_validate_order_field():
    assert validate_order_field('id') == Post.c.id
    assert validate_order_field('title') == Post.c.title
    assert validate_order_field('url') == Post.c.url
    with pytest.raises(HTTPBadRequestJSON):
        validate_order_field(None)
        validate_order_field('not_exists')


def test_validate_order_type():
    assert validate_order_type('asc') == 'asc'
    assert validate_order_type('desc') == 'desc'
    with pytest.raises(HTTPBadRequestJSON):
        validate_order_type(None)
        validate_order_type('not_exists')
