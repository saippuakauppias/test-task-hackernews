from sqlalchemy import create_engine, MetaData

from . import config
from .models import Post


DSN = config.DB_DSN.format(**config.as_dict())


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[Post])


def get_engine():
    return create_engine(DSN)
