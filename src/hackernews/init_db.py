from sqlalchemy import create_engine, MetaData

from . import config
from .models import item

DSN = config.DB_DSN.format(**config)


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[item])


if __name__ == '__main__':
    engine = create_engine(DSN)

    create_tables(engine)

    from time import sleep
    sleep(1000000)
