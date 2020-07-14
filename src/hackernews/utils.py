import json
import datetime
import functools


def datetime_json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()


json_dumps = functools.partial(json.dumps, default=datetime_json_converter)
