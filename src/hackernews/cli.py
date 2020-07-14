import asyncio
import logging

import click
from aiohttp import web

from .app import get_app
from .helpers.sync import sync
from .parsers import parse_topstories
from .db import get_engine, create_tables


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(name)s  - %(message)s',
)
logger = logging.getLogger(__name__)


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
    print(parse_topstories())
