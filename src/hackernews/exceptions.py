from aiohttp.web import HTTPBadRequest

from .utils import json_dumps


class HTTPBadRequestJSON(HTTPBadRequest):

    def __init__(self, *, headers=None, reason=None, body=None, text=None,
                 content_type=None):
        super().__init__(headers=headers, reason=reason, body=body,
                         text=text, content_type=content_type)
        self.text = json_dumps({'error': text})
        self.content_type = 'application/json'


class ParseError(RuntimeError):
    pass
