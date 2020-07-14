import json
import datetime
import functools

from aiohttp.web import HTTPBadRequest


def datetime_json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()


json_dumps = functools.partial(json.dumps, default=datetime_json_converter)


def validate_param_int(param, error_text, disallow_zero=True):
    try:
        param = int(param)
        param = max(0, param)
        param = min(param, 100)
        if disallow_zero and not param:
            raise ValueError()
    except ValueError:
        data = {'error': error_text}
        data = json_dumps(data)
        raise HTTPBadRequest(body=data)

    return param
