from aiohttp import web

from .routes import routes
from .db import (init_db, close_db)


async def get_app():
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app
