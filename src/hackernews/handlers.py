from aiohttp import web

from .models import Post
from .utils import (json_dumps, validate_param_int)


async def posts(request):
    limit = request.query.get('limit', 5)
    limit = validate_param_int(limit, 'wrong value in limit param')

    offset = request.query.get('offset', 0)
    offset = validate_param_int(offset, 'wrong value in offset param', False)

    async with request.app['db'].acquire() as conn:
        stmt = Post.select().with_only_columns([
            Post.c.id,
            Post.c.title,
            Post.c.url
        ]).limit(limit)

        if offset:
            stmt = stmt.offset(offset)

        cursor = await conn.execute(stmt)
        records = await cursor.fetchall()
        posts = [dict(p) for p in records]
        return web.json_response(posts, dumps=json_dumps)
