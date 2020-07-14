import asyncio

import click
from aiohttp import web

from . import logger
from .app import get_app
from .helpers.sync import sync
from .parsers import parse_topstories
from .db import get_engine, create_tables, create_posts


@click.group()
def cli():
    pass


@cli.command()
@click.option('--host', type=str, default='127.0.0.1')
@click.option('--port', type=int, default=8080)
@sync
async def serve(host: str, port: int) -> None:
    runner = web.AppRunner(await get_app())
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f'Listening on {host}:{port}')
    await asyncio.Future()


@cli.command()
def init():
    engine = get_engine()
    create_tables(engine)
    logger.info('Tables created successfully')


@cli.command()
def parse():
    posts = parse_topstories()

    engine = get_engine()
    conn = engine.connect()
    try:
        create_posts(conn, posts)
    finally:
        conn.close()
