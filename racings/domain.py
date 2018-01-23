import sqlalchemy as sa
from sqlalchemy import (BLOB, Column, DateTime, ForeignKey, Integer, String,
                        Table, Text, func)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class Body(BaseModel):
    __tablename__ = 'body'
    id = Column(Integer, primary_key=True)
    name =  Column(String(256))
    phone = Column(String(11) )
    email = Column(String(256))
    address = Column(Text)


class User(BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, ForeignKey('body.id'), primary_key=True)
    login = Column(String(128))
    pw = Column(String(128))


class Manufacturer(BaseModel):
    __tablename__ = 'mfr'
    id = Column(Integer, ForeignKey('body.id'), primary_key=True)


class Homologation(BaseModel):
    __tablename__ = 'homologation'
    id = Column(Integer, primary_key=True)
    code = Column(String(64), nullable=False)


class LicenseBase(BaseModel):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    @declared_attr
    def licensee(cls):
        return Column(Integer, ForeignKey('body.id'))
    @declared_attr
    def issuer(cls):
        return Column(Integer, ForeignKey('body.id'))
    valid_until = Column(DateTime)


class DriversLic(LicenseBase):
    __tablename__ = 'drvlic'
    pass


class ScrutLic(LicenseBase):
    __tablename__ = 'scrlic'
    pass


class Picture(BaseModel):
    __tablename__ = 'pic'
    id = Column(Integer, primary_key=True)
    data = Column(BLOB)


class CarPassport(BaseModel):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('body.id'))
    valid_until = Column(DateTime)
    mfr = Column(Integer, ForeignKey('mfr.id'))
    #  relationships
    #  ---
    #  that's a shitty concept; screws dependencies;
    #  could've defined it in 'CarPhotos' but it aint fix anything solution
    photos = relationship('Picture',
                          secondary='carphoto',
                          backref='car')


class CarPhotos(BaseModel):
    __tablename__ = 'carphoto'
    car = Column(Integer, ForeignKey('car.id'), primary_key=True)
    photo = Column(Integer, ForeignKey('pic.id'), primary_key=True)
