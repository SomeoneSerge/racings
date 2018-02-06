from sqlalchemy import Column, String, Text, ForeignKey, Table, join, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, column_property


def add_models(domain):
    """add_models(simple_data.Domain)
    Adds"""

    meta = domain.Base.metadata

    class Person(domain.Base):
        """Person data model (includes legal bodies)"""
        __tablename__ = 'person'
        id = Column(domain.PK_TYPE, primary_key=True, unique=True)
        name = Column(Text)
        phone = Column(String(15))
        email = Column(Text)
        address = Column(Text)

    doctype = Table('doctype', meta,
                    Column('id', domain.PK_TYPE,
                           primary_key=True, unique=True),
                    Column('name', Text))
    doc = Table('doc', meta,
                Column('id', domain.PK_TYPE, primary_key=True, unique=True),
                Column('name', Text, unique=True),
                Column('doctype_id', domain.PK_TYPE,
                       ForeignKey('doctype.id')),
                Column('issuer_id', domain.PK_TYPE,
                       ForeignKey('person.id')))

    def var_columns():
        return (
            Column('id', domain.PK_TYPE, primary_key=True, unique=True),
            Column('name', Text, nullable=False),
            Column('doctype_id', domain.PK_TYPE,
                   ForeignKey('doctype.id')),
        )
    numvar = Table('numvar', meta,
                   *var_columns(),)
    refvar = Table('refvar', meta,
                   *var_columns(),
                   Column('reftype_id', domain.PK_TYPE,
                          ForeignKey('doctype.id'),))

    def rec_columns(vartype_id):
        return (
            # adding an artificial id because of Eve
            Column('id', domain.PK_TYPE, unique=True),
            PrimaryKeyConstraint('id'),
            Column('var_id', domain.PK_TYPE,
                   ForeignKey(vartype_id),),
            Column('doc_id', domain.PK_TYPE,
                   ForeignKey('doc.id'),)
        )
    numrec = Table('numrec', meta,
                   *rec_columns('numvar.id'),
                   Column('value', domain.Numeric,
                          nullable=False))
    refrec = Table('refrec', meta,
                   *rec_columns('refvar.id'),
                   Column('ref_id', domain.PK_TYPE,
                          ForeignKey('doc.id')))
    numerical_records = join(numvar, numrec)
    referential_records = join(refvar, refrec)
    # referential_records = (
    #     select([referential_records, doc.c.name])
    #     .select_from(join(referential_records, doc,
    #                       refrec.c.ref_id == doc.c.id))
    #     .alias()
    # )

    class DocType(domain.Base):
        __table__ = doctype
        instances = relationship('Doc', back_populates='doctype')

    class Doc(domain.Base):
        __table__ = doc
        doctype = relationship('DocType', uselist=False,
                               back_populates='instances',
                               foreign_keys=[doc.c.doctype_id])
        issuer = relationship('Person', uselist=False,
                              foreign_keys=[doc.c.issuer_id])

    class ReferentialVar(domain.Base):
        __table__ = refvar
        reftype = relationship('DocType', uselist=False,
                               foreign_keys=[refvar.c.reftype_id])
        records = relationship('RefRec', back_populates='var')

    class RefRec(domain.Base):
        __table__ = referential_records
        var_id = column_property(refrec.c.var_id, refvar.c.id)
        var = relationship('ReferentialVar', uselist=False,
                           foreign_keys=[refrec.c.var_id],
                           back_populates='records')
        value = relationship('Doc', uselist=False,
                             foreign_keys=[refrec.c.ref_id])
        __mapper_args__ = {
            'primary_key': [refrec.c.id]
        }

    class NumericVar(domain.Base):
        __table__ = numvar
        records = relationship('NumRec', back_populates='var')

    class NumRec(domain.Base):
        __table__ = numerical_records
        var_id = column_property(numrec.c.var_id, numvar.c.id)
        var = relationship('NumericVar', uselist=False,
                           foreign_keys=[numrec.c.var_id],
                           back_populates='records')
        __mapper_args__ = {
            'primary_key': [numrec.c.id]
        }

    domain.add_model('Person', Person, Person.id)
    domain.add_model('Doc', Doc, Doc.id)
    domain.add_model('DocType', DocType, DocType.id)
    domain.add_model('RefVar', ReferentialVar, ReferentialVar.id)
    domain.add_model('RefRec', RefRec, RefRec.id)
    domain.add_model('NumVar', NumericVar, NumericVar.id)
    domain.add_model('NumRec', NumRec, NumRec.id)
    return domain
