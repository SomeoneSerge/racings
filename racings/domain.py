import sqlalchemy as sa
from sqlalchemy import (BLOB, Column, DateTime, ForeignKey, Integer, String,
                        Table, Text, func)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship

from racings.db import Base, BaseModel
from racings.auth import UserBase

#   Quite nasty hack. Will get fixed once I get rid of SQLAlchemy
EXPOSED = dict()


class ArtificialId(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class TimeSpanning(Base):
    __abstract__ = True
    since = Column(DateTime)
    until = Column(DateTime)


# Based on: http://taketwoprogramming.blogspot.com/2009/08/reusable-sqlalchemy-models.html
def build_homologation(homologatable, column='homologation'):
    metadata = Base.metadata
    h_class_name = homologatable.capitalize() + column.capitalize()
    h_table_name = homologatable + '_' + column
    h_class = type(h_class_name, (BaseModel,),
                   dict(__tablename__=h_table_name,
                        id=Column(Integer, primary_key=True),
                        code=Column(Text, unique=True),
                        federation=Column(Text), # Consider maintaining a set of those valid
                        valid_thru=Column(DateTime)))
    EXPOSED[h_table_name] = h_class
    return Column(Integer, ForeignKey(h_table_name + '.id'))

def has_owner(column='owner'):
    def _has_owner(clz):
        setattr(clz, column,
                Column(Integer, ForeignKey('body.id')))
        return clz
    return _has_owner

def signed_by(signer_table,
              column_issuer='issuer',
              column_issued='issued'):
    def _signed(clz):
        # The issuer
        setattr(clz, column_issuer,
                Column(Integer, ForeignKey(signer_table + '.id'), nullable=False))
        # The date the document was issued
        setattr(clz, column_issued,
                Column(DateTime, nullable=False))
        return clz
    return _signed


class Body(BaseModel, ArtificialId):
    __tablename__ = 'body'
    name =  Column(String(256))
    phone = Column(String(11) )
    email = Column(String(256))
    address = Column(Text)
EXPOSED['bodies'] = Body


class User(BaseModel, UserBase):
    __tablename__ = 'user'
    id = Column(Integer, ForeignKey('body.id'), primary_key=True)
    login = Column(String(128))
    pw = Column(String(128))

    
EXPOSED['users'] = User


class Part(BaseModel, ArtificialId):
    __tablename__ = 'part'
    name = Column(Text)
EXPOSED['parts'] = Part

class LicenseBase(BaseModel, ArtificialId):
    __abstract__ = True
    @declared_attr
    def licensee(cls):
        return Column(Integer, ForeignKey('body.id'))
    @declared_attr
    def issuer(cls):
        return Column(Integer, ForeignKey('body.id'))
    valid_until = Column(DateTime)


class DriversLic(LicenseBase):
    __tablename__ = 'driver'
    pass
EXPOSED['drivers'] = DriversLic


class ScrutLic(LicenseBase):
    __tablename__ = 'scrutineer'
EXPOSED['scrutineers'] = ScrutLic


class Picture(BaseModel, ArtificialId):
    __tablename__ = 'pic'
    data = Column(BLOB)
EXPOSED['pics'] = Picture


class Make(BaseModel, ArtificialId):
    __tablename__ = 'make'
    name = Column(Text)
EXPOSED['makes'] = Make


class WheelDrive(BaseModel, ArtificialId):
    __tablename__ = 'wheeldrive'
    name = Column(Text, unique=True)
EXPOSED['wheeldrives'] = WheelDrive


class AutomobilePhotos(BaseModel):
    __tablename__ = 'automobilephoto'
    automobile = Column(Integer, ForeignKey('automobile.id'), primary_key=True)
    photo = Column(Integer, ForeignKey('pic.id'), primary_key=True)

@has_owner()
@signed_by('scrutineer')
class Automobile(BaseModel, ArtificialId):
    __tablename__ = 'automobile'
    code = Column(Text, unique=True)
    valid_until = Column(DateTime)
    make = Column(Integer, ForeignKey('make.id'))
    chassis = Column(Text)
    engine = Column(Text)
    engine_year = Column(Integer)
    cyl_cap = Column(Integer)
    drive = Column(Integer, ForeignKey('wheeldrive.id'))
    homologation = build_homologation('automobile')

    #  relationships
    #  ---
    #  that's a shitty concept; screws dependencies;
    #  could've defined it in 'AutomobilePhotos' but it aint fix anything solution
    photos = relationship('Picture',
                          secondary='automobilephoto',
                          backref='automobile')
EXPOSED['automobiles'] = Automobile


class Group(BaseModel, ArtificialId):
    __tablename__ = 'group'
    name = Column(Text, unique=True)
EXPOSED['groups'] = Group


class Event(BaseModel, ArtificialId, TimeSpanning):
    __tablename__ = 'event'
    tech_delegate = Column(Integer, ForeignKey('scrutineer.id'))
    status = Column(Text) # So far
EXPOSED['events'] = Event


class Competition(BaseModel, ArtificialId, TimeSpanning):
    __tablename__ = 'competition'
    event = Column(Integer, ForeignKey('event.id'))
    group = Column(Integer, ForeignKey('group.id'))
EXPOSED['competitions'] = Competition


# Nasty hack: python-eve allows only single pk so hence an artificial
class Lap(BaseModel, TimeSpanning, ArtificialId):
    __tablename__ = 'lap'
    competition = Column(Integer,
                         ForeignKey('competition.id'),
    )
    serial = Column(Integer)
EXPOSED['laps'] = Lap


@signed_by('scrutineer')
class Inspection(BaseModel):
    __tablename__ = 'inspection'
    id = Column(Integer, primary_key=True)

