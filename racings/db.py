import sqlalchemy as sa
from sqlalchemy import (BLOB, Column, DateTime, ForeignKey, Integer, String,
                        Table, Text, func)
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))
