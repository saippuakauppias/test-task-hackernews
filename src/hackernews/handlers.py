from aiohttp import web

from .models import Post
from .utils import json_dumps
from .validators import  (validate_int, validate_order_field,
                          validate_order_type)


async def posts(request):
    limit = request.query.get('limit', 5)
    limit = validate_int(limit, 'wrong value in limit param', max_value=100)

    offset = request.query.get('offset', 0)
    offset = validate_int(offset, 'wrong value in offset param',
                          disallow_zero=False)

    order_field = request.query.get('order', None)
    order_field = validate_order_field(order_field)

    order_type = request.query.get('order_type', 'asc')
    order_type = validate_order_type(order_type)

    async with request.app['db'].acquire() as conn:
        stmt = Post.select().with_only_columns([
            Post.c.id,
            Post.c.title,
            Post.c.url
        ]).limit(limit)

        if offset:
            stmt = stmt.offset(offset)

        if order_field is not None:
            if order_type is not None:
                order_field = getattr(order_field, order_type)
                order_field = order_field()
            stmt = stmt.order_by(order_field)

        cursor = await conn.execute(stmt)
        records = await cursor.fetchall()
        posts = [dict(p) for p in records]
        return web.json_response(posts, dumps=json_dumps)
