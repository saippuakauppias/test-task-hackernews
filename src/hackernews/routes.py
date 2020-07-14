from aiohttp import web

from .handlers import posts


routes = [
    web.get('/posts', posts),
]
