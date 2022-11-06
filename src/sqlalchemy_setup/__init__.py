import sqlalchemy as sa
from sqlalchemy import MetaData, orm

from .base import Base as _Base
from .get_or_create import get_or_create as _get_or_create

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Database:
    inited = False

    def __init__(self, url, **engine_args):
        self.engine = sa.create_engine(url, **engine_args)
        self.Session = orm.sessionmaker(bind=self.engine)
        self.session = orm.scoped_session(self.Session)
        self.session.get_or_create = lambda *args, **kwargs: _get_or_create(
            *args, session=self.session, **kwargs
        )

        self.Base: _Base = orm.declarative_base(cls=_Base, metadata=meta)
        self.Base.query = self.session.query_property()

        if not self.inited:
            self.init()
            self.inited = True

    def init(self):
        self.Base.metadata.create_all(bind=self.engine)

    def teardown(self, exception=None):
        self.session.remove()
