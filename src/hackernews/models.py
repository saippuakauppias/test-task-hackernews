from sqlalchemy import (MetaData, Table, Column, Integer, String, DateTime,
                        text)


meta = MetaData()


Post = Table(
    'post',
    meta,

    Column('id', Integer, primary_key=True),
    Column('post_id', String(10), nullable=False, unique=True),
    Column('title', String(512), nullable=False),
    Column('url', String(256), nullable=False),
    Column('created', DateTime, nullable=False,
           server_default=text('NOW()'))
)
