import sqlalchemy as sa
from sqlalchemy import orm

from sqlalchemy_setup.utils import str_format


class Base:
    @orm.declared_attr
    def __tablename__(cls):
        name = cls.__name__
        name = str_format.pluralize(name)
        name = str_format.snake_case(name)
        return name

    id = sa.Column(sa.Integer, primary_key=True)

    def __repr__(self):
        if isinstance(self, type):
            class_ = self
        else:
            class_ = type(self)
        header = [class_.__name__]
        if getattr(self, "id"):
            header.append(f"#{self.id}")
        body = [
            f"{column.name}={getattr(self, column.name)}"
            for column in class_.__table__.columns
            if column.name != "id"
        ]
        return "<{header}: {body}>".format(
            header=" ".join(header), body=", ".join(body)
        )
