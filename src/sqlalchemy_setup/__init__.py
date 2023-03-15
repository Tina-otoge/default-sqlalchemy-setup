import sqlalchemy as sa
from sqlalchemy import MetaData, orm

from .base import Base as _Base
from .get_or_create import get_or_create as _get_or_create


class Database:
    def __init__(self, url, id=None, **engine_args):
        meta = MetaData(
            naming_convention={
                "ix": "ix_%(column_0_label)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(column_0_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "pk": "pk_%(table_name)s",
            }
        )
        self.inited = False
        self.engine = sa.create_engine(url, **engine_args)
        self.Base: _Base = orm.declarative_base(cls=_Base, metadata=meta)
        self.Base.metadata.bind = self.engine

    def init(self):
        if self.inited:
            return
        print("Initializing database", self.engine)
        self.Base.metadata.create_all(bind=self.engine)
        self.inited = True
