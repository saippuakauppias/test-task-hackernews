from .models import Post
from .exceptions import HTTPBadRequestJSON


def validate_int(param, error_text, max_value=None, disallow_zero=True):
    try:
        param = int(param)
        param = max(0, param)
        if max_value is not None:
            param = min(param, max_value)
        if disallow_zero and not param:
            raise ValueError()
    except ValueError:
        raise HTTPBadRequestJSON(text=error_text)

    return param


def validate_order_field(order_field):
    order_mapping = {
        'id': Post.c.id,
        'title': Post.c.title,
        'url': Post.c.url
    }

    if order_field:
        order_field_keys = order_mapping.keys()
        if order_field not in order_field_keys:
            order_field_keys = ','.join(order_field_keys)
            raise HTTPBadRequestJSON(
                text=f'order param accept only: {order_field_keys}')
        else:
            order_field = order_mapping[order_field]

    return order_field


def validate_order_type(order_type):
    order_type_allowed = ['asc', 'desc']
    if order_type not in order_type_allowed:
        order_type_allowed = ','.join(order_type_allowed)
        raise HTTPBadRequestJSON(
            text=f'order_type param accept only: {order_type_allowed}')

    return order_type
