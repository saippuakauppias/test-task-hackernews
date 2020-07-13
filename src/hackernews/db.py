from sqlalchemy import create_engine, MetaData

from hackernews import config
from hackernews.models import item


DSN = config.DB_DSN.format(**config.as_dict())


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[item])


def get_engine():
    return create_engine(DSN)
