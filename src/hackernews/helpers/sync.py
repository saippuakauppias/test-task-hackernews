import asyncio
from functools import wraps


def sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(
            func(*args, **kwargs))
    return wrapper
