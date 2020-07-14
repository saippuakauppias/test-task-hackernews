import logging

from simple_settings import LazySettings


config = LazySettings('hackernews.settings')


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(name)s  - %(message)s',
)
logger = logging.getLogger(__name__)
