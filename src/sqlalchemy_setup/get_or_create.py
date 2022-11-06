from dataclasses import dataclass


@dataclass
class Result:
    obj: object
    created: bool = False


def get_or_create(model, filter_cols=None, session=None, **kwargs):
    filter_cols = filter_cols or kwargs.keys()
    obj = (
        session.query(model)
        .filter_by(**{col: kwargs[col] for col in filter_cols})
        .first()
    )
    if obj:
        return Result(obj)
    obj = model(**kwargs)
    session.add(obj)
    return Result(obj, True)
