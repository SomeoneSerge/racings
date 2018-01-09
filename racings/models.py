import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey


def base_schema(Base):
    class Event(Base):
        id = Column(Integer, primary_key=True)
        name = Column(sa.String(256))
        tech_delegate = Column(
            Integer,
            ForeignKey('Scrutineer.id'))

    class Competition(Base):
        id = Column(Integer, primary_key=True)
        event = Column(Integer, ForeignKey('Event.id'))
        group = Column(Integer, ForeignKey('Group.id'))

    class Lap(Base):
        competition = Column(
            Integer,
            ForeignKey('Competition.id'),
            primary_key=True)
        lap_no = Column(Integer, primary_key=True)

    class Scrutineer(Base):
        id = Column(Integer)
        body = Column(
            Integer,
            ForeignKey('Body.id'))
        valid_since = Column(sa.Date)
        valid_until = Column(sa.Date)

    class Scrutineering(Base):
        pass
