from aiohttp import web

from .models import Post
from .utils import json_dumps


async def posts(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(Post.select().with_only_columns([
            Post.c.id,
            Post.c.title,
            Post.c.url
        ]))
        records = await cursor.fetchall()
        posts = [dict(p) for p in records]
        return web.json_response(posts, dumps=json_dumps)
