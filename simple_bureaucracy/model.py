from sqlalchemy import (Column, ForeignKey, PrimaryKeyConstraint, String,
                        select, Table, Text, join)
from sqlalchemy.orm import column_property, relationship


def add_models(domain):
    """add_models(simple_data.Domain)
    Adds"""

    meta = domain.Base.metadata

    person = Table(
        'person',
        meta,
        *domain.common_columns(),
        Column('id', domain.PK_TYPE, primary_key=True, unique=True),
        Column('name', Text, nullable=False),
        Column('phone', String(15)),
        Column('email', Text),
        Column('address', Text),
    )

    role = Table(
        'role',
        meta,
        *domain.common_columns(),
        Column('id', domain.PK_TYPE, primary_key=True, unique=True),
        Column('name', Text, nullable=False),
    )

    class StrMixin:
        def __str__(self):
            if hasattr(self, 'name'):
                return self.name
            else:
                return self.__name__

    doctype = Table('doctype', meta, *domain.common_columns(),
                    Column(
                        'id', domain.PK_TYPE, primary_key=True, unique=True),
                    Column('managed_by_role_id', domain.PK_TYPE,
                           ForeignKey('role.id')), Column('name', Text))
    doc = Table('doc', meta, *domain.common_columns(),
                Column('id', domain.PK_TYPE, primary_key=True, unique=True),
                Column('name', Text, nullable=False),
                Column('doctype_id', domain.PK_TYPE, ForeignKey('doctype.id')),
                Column('issuer_id', domain.PK_TYPE, ForeignKey('person.id')))

    def var_columns():
        return (
            *domain.common_columns(),
            Column('id', domain.PK_TYPE, primary_key=True, unique=True),
            Column('name', Text, nullable=False),
            Column(
                'doctype_id',
                domain.PK_TYPE,
                ForeignKey('doctype.id'),
                nullable=False),
        )

    numvar = Table('numvar', meta, *var_columns())
    personvar = Table('personvar', meta, *var_columns())
    refvar = Table('refvar', meta, *var_columns(),
                   Column(
                       'valuetype_id',
                       domain.PK_TYPE,
                       ForeignKey('doctype.id'),
                   ))

    def rec_columns(vartype_id):
        return (
            *domain.common_columns(),
            # adding an artificial id because of Eve
            Column('id', domain.PK_TYPE, unique=True),
            Column(
                'var_id',
                domain.PK_TYPE,
                ForeignKey(vartype_id),
                nullable=False),
            Column(
                'doc_id', domain.PK_TYPE, ForeignKey('doc.id'),
                nullable=False))

    numrec = Table('numrec', meta, *rec_columns('numvar.id'),
                   Column('value', domain.Numeric, nullable=False))
    personrec = Table('personrec', meta, *rec_columns('personvar.id'),
                      Column(
                          'person_id',
                          domain.PK_TYPE,
                          ForeignKey('person.id'),
                          nullable=False))
    refrec = Table(
        'refrec',
        meta,
        *rec_columns('refvar.id'),
        Column('ref_id', domain.PK_TYPE, ForeignKey('doc.id'), nullable=False),
    )

    class Person(domain.Base):
        """Person data model (includes legal bodies)"""
        __table__ = person

        def __str__(self):
            return '{} <{}>'.format(self.name, self.email)

    class Role(domain.Base, StrMixin):
        __table__ = role

    class DocType(domain.Base, StrMixin):
        __table__ = doctype
        instances = relationship('Doc', back_populates='doctype')
        ref_variables = relationship(
            'RefVar',
            back_populates='doctype',
            foreign_keys=[refvar.c.doctype_id])
        num_variables = relationship(
            'NumVar',
            back_populates='doctype',
            foreign_keys=[numvar.c.doctype_id])
        person_variables = relationship(
            'PersonVar',
            back_populates='doctype',
            foreign_keys=[personvar.c.doctype_id])
        managed_by = relationship(
            'Role', uselist=False, foreign_keys=[doctype.c.managed_by_role_id])

    class Doc(domain.Base, StrMixin):
        __table__ = doc
        doctype = relationship(
            'DocType',
            uselist=False,
            back_populates='instances',
            foreign_keys=[doc.c.doctype_id])
        issuer = relationship(
            'Person', uselist=False, foreign_keys=[doc.c.issuer_id])
        ref_records = relationship(
            'RefRec', back_populates='doc', foreign_keys=[refrec.c.doc_id])
        num_records = relationship(
            'NumRec', back_populates='doc', foreign_keys=[numrec.c.doc_id])
        person_records = relationship(
            'PersonRec',
            back_populates='doc',
            foreign_keys=[personrec.c.doc_id])

    class RefVar(domain.Base, StrMixin):
        __table__ = refvar
        valuetype = relationship(
            'DocType', uselist=False, foreign_keys=[refvar.c.valuetype_id])
        doctype = relationship(
            'DocType', uselist=False, foreign_keys=[refvar.c.doctype_id])

    class RefRec(domain.Base, StrMixin):
        __table__ = refrec
        var_id = column_property(refrec.c.var_id, refvar.c.id)
        var = relationship(
            'RefVar',
            uselist=False,
            foreign_keys=[refrec.c.var_id],
        )
        doc = relationship(
            'Doc',
            uselist=False,
            foreign_keys=[refrec.c.doc_id],
            back_populates='ref_records')
        value = relationship(
            'Doc', uselist=False, foreign_keys=[refrec.c.ref_id])
        __mapper_args__ = {'primary_key': [refrec.c.id]}

    class NumVar(domain.Base, StrMixin):
        __table__ = numvar
        doctype = relationship(
            'DocType', uselist=False, foreign_keys=[numvar.c.doctype_id])

    class PersonVar(domain.Base, StrMixin):
        __table__ = personvar
        doctype = relationship(
            'DocType', uselist=False, foreign_keys=[personvar.c.doctype_id])

    class NumRec(domain.Base, StrMixin):
        __table__ = numrec
        var_id = column_property(numrec.c.var_id, numvar.c.id)
        var = relationship(
            'NumVar',
            uselist=False,
            foreign_keys=[numrec.c.var_id],
        )
        doc = relationship(
            'Doc',
            uselist=False,
            foreign_keys=[numrec.c.doc_id],
            back_populates='num_records')
        __mapper_args__ = {'primary_key': [numrec.c.id]}

    class PersonRec(domain.Base, StrMixin):
        __table__ = personrec
        var_id = column_property(personrec.c.var_id, personvar.c.id)
        var = relationship(
            'PersonVar',
            uselist=False,
            # back_populates='records',
            foreign_keys=[personrec.c.var_id],
        )
        doc = relationship(
            'Doc',
            uselist=False,
            foreign_keys=[personrec.c.doc_id],
            back_populates='person_records')
        value = relationship(
            'Person',
            uselist=False,
            foreign_keys=[personrec.c.person_id],
        )
        __mapper_args__ = {'primary_key': [personrec.c.id]}

    domain.add_model('Person', Person, Person.id)
    domain.add_model('Role', Role, Role.id)
    domain.add_model('Doc', Doc, Doc.id)
    domain.add_model('DocType', DocType, DocType.id)
    domain.add_model('RefVar', RefVar, RefVar.id)
    domain.add_model('RefRec', RefRec, RefRec.id)
    domain.add_model('NumVar', NumVar, NumVar.id)
    domain.add_model('NumRec', NumRec, NumRec.id)
    domain.add_model('PersonVar', PersonVar, PersonVar.id)
    domain.add_model('PersonRec', PersonRec, PersonRec.id)
    return domain
