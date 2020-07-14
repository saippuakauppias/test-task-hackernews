from sqlalchemy import create_engine, MetaData, select

from . import (config, logger)
from .models import Post


DSN = config.DB_DSN.format(**config.as_dict())


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[Post])


def get_engine():
    return create_engine(DSN)


def create_posts(connect, posts):
    # skip exists (without update)
    exists = connect.execute(
        select(
            [Post.c.post_id],
            Post.c.post_id.in_(posts.keys())
        )
    ).fetchall()
    posts_skipped = len(exists)
    for post_exist in exists:
        posts.pop(post_exist.post_id)

    # add new
    posts_inserted = len(posts)
    if posts:
        connect.execute(Post.insert(), list(posts.values()))

    logger.info(
        f'Inserted posts: {posts_inserted} | Skipped posts: {posts_skipped}')
