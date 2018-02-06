from sqlalchemy import Column, func, DateTime, String
from modular_sqla import Domain
from sqlalchemy.ext.declarative import declarative_base


def common_columns():
    _created = Column('_created', DateTime, default=func.now())
    _updated = Column(
        '_updated', DateTime, default=func.now(), onupdate=func.now())
    _etag = Column('_etag', String(40))
    return [_created, _updated, _etag]


DOMAIN = Domain(common_columns=common_columns)
DOMAIN.use_package('simple_bureaucracy')

EXPOSED = DOMAIN.models.copy()
