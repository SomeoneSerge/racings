from sqlalchemy import (Column, ForeignKey, PrimaryKeyConstraint, String,
                        select, Table, Text, join)
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.ext.declarative import declared_attr


def add_models(domain):
    """add_models(simple_data.Domain)
    Adds"""

    Base = domain.Base

    class IdMixin:
        id = Column(domain.PK_TYPE, primary_key=True, unique=True)

    class StrMixin:
        def __str__(self):
            if hasattr(self, 'name'):
                return self.name
            else:
                return self.__name__

    class Person(Base, IdMixin):
        __tablename__ = 'person'
        name = Column(Text, nullable=False)
        phone = Column(String(15))
        email = Column(Text)
        address = Column(Text)

        def __str__(self):
            return '{} <{}>'.format(self.name, self.email)

    class DocType(Base, IdMixin, StrMixin):
        __tablename__ = 'doctype'
        name = Column(Text)

        instances = relationship('Doc', back_populates='doctype')
        # refvar = relationship(
        #     'RefVar',
        #     back_populates='doctype',)
        # numvar = relationship(
        #     'NumVar',
        #     back_populates='doctype',)
        # personvar = relationship(
        #     'PersonVar',
        #     back_populates='doctype',)

    class Doc(Base, IdMixin, StrMixin):
        __tablename__ = 'doc'
        name = Column(Text, unique=True, nullable=False)
        doctype_id = Column(domain.PK_TYPE, ForeignKey('doctype.id'))
        issuer_id = Column(domain.PK_TYPE, ForeignKey('person.id'))
        doctype = relationship(
            DocType,
            uselist=False,
            back_populates='instances',
            foreign_keys=doctype_id)
        issuer = relationship(
            'Person', uselist=False, foreign_keys=[issuer_id])
        # refrec = relationship(
        #     'RefRec', back_populates='doc', foreign_keys='refrec.doc_id')
        # numrec = relationship(
        #     'NumRec', back_populates='doc', foreign_keys='numrec.doc_id')
        # personrec = relationship(
        #     'PersonRec', back_populates='doc',
        #     foreign_keys='personrec.doc_id')

    class VarMixin:
        name = Column(Text, unique=True, nullable=False),

        @declared_attr
        def doctype_id(cls):
            return Column(
                domain.PK_TYPE, ForeignKey('doctype.id'), nullable=False)

        @declared_attr
        def doctype(cls):
            return relationship(
                'DocType',
                uselist=False,
                back_populates=cls.__tablename__,
                foreign_keys=cls.__tablename__ + '.doctype_id')

    class NumVar(Base, VarMixin, IdMixin):
        __tablename__ = 'numvar'

    class PersonVar(Base, VarMixin, IdMixin):
        __tablename__ = 'personvar'

    class RefVar(Base, VarMixin, IdMixin):
        __tablename__ = 'refvar'
        valuetype_id = Column(
            'valuetype_id',
            domain.PK_TYPE,
            ForeignKey('doctype.id'),
        )
        valuetype = relationship(
            DocType,
            uselist=False,
            foreign_keys=__tablename__ + '.valuetype_id')

    class RecMixin:
        # adding an artificial id because of Eve

        @declared_attr
        def doc_id(cls):
            doc_id = Column(
                'doc_id', domain.PK_TYPE, ForeignKey('doc.id'), nullable=False)
            return doc_id

        @declared_attr
        def doc(cls):
            return relationship(
                Doc,
                uselist=False,
                foreign_keys=cls.__tablename__ + '.doc_id',
                back_populates=cls.__tablename__)

    class NumRec(Base, RecMixin, IdMixin):
        __tablename__ = 'numrec'
        value = Column(domain.Numeric, nullable=False)
        var_id = Column(
            'var_id', domain.PK_TYPE, ForeignKey('numvar.id'), nullable=False)
        var = relationship(
            NumVar,
            uselist=False,
            # back_populates='records',
            foreign_keys='numrec.var_id',
        )

    class PersonRec(Base, RecMixin, IdMixin):
        __tablename__ = 'personrec'
        person_id = Column(
            'person_id',
            domain.PK_TYPE,
            ForeignKey('person.id'),
            nullable=False)
        var_id = Column(
            'var_id',
            domain.PK_TYPE,
            ForeignKey('personvar.id'),
            nullable=False)
        var = relationship(
            PersonVar,
            uselist=False,
            # back_populates='records',
            foreign_keys='personrec.var_id',
        )
        value = relationship(
            Person,
            uselist=False,
            foreign_keys='personrec.person_id',
        )

    class RefRec(Base, RecMixin, IdMixin):
        __tablename__ = 'refrec'
        ref_id = Column(
            'ref_id', domain.PK_TYPE, ForeignKey('doc.id'), nullable=False)
        var_id = Column(
            'var_id', domain.PK_TYPE, ForeignKey('refvar.id'), nullable=False)
        var = relationship(
            RefVar,
            uselist=False,
            foreign_keys='refrec.var_id',
        )
        value = relationship(Doc, uselist=False, foreign_keys='refrec.ref_id')

    domain.add_model('Person', Person, Person.id)
    domain.add_model('Doc', Doc, Doc.id)
    domain.add_model('DocType', DocType, DocType.id)
    domain.add_model('RefVar', RefVar, RefVar.id)
    domain.add_model('RefRec', RefRec, RefRec.id)
    domain.add_model('NumVar', NumVar, NumVar.id)
    domain.add_model('NumRec', NumRec, NumRec.id)
    domain.add_model('PersonVar', PersonVar, PersonVar.id)
    domain.add_model('PersonRec', PersonRec, PersonRec.id)
    return domain
