from sqlalchemy import Column, String, Text, ForeignKey, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.declarative import declared_attr


def add_models(domain):
    """add_models(simple_data.Domain)
    Adds"""

    class Person(domain.Base):
        """Person data model (includes legal bodies)"""
        __tablename__ = 'person'
        id = Column(domain.PK_TYPE, primary_key=True)
        name = Column(Text)
        phone = Column(String(15))
        email = Column(Text)
        address = Column(Text)

    class DocType(domain.Base):
        __tablename__ = 'doctype'
        id = Column(domain.PK_TYPE, primary_key=True)
        name = Column(Text)
        instances = relationship('Doc', back_populates='doctype')

    class Doc(domain.Base):
        __tablename__ = 'doc'
        id = Column(domain.PK_TYPE, primary_key=True)
        doctype_id = Column('type', domain.PK_TYPE,
                            ForeignKey('doctype.id'))
        doctype = relationship('DocType', uselist=False,
                               back_populates='instances',
                               foreign_keys=[doctype_id])
        issuer_id = Column('issuer', domain.PK_TYPE)
        issuer = relationship('Person', uselist=False,
                              foreign_keys=[issuer_id])

    class DocVar(domain.Base):
        __tablename__ = 'docvar'
        id = Column(domain.PK_TYPE, primary_key=True)
        name = Column(Text)
        doctype_id = Column('doctype',
                            domain.PK_TYPE,
                            ForeignKey('doctype.id'))
        doctype = relationship('DocType',
                               uselist=False,
                               foreign_keys=[doctype_id])
        kind = Column(String(50))

        @declared_attr
        def __mapper_args__(cls):
            args = {'polymorphic_identity': cls.__tablename__}
            if cls.__tablename__ == 'docvar':
                args['polymorphic_on'] = cls.kind
            return args

    class ReferentialVar(DocVar):
        __tablename__ = 'refvar'
        id = Column(domain.PK_TYPE,
                    ForeignKey('docvar.id'),
                    primary_key=True)
        reftype_id = Column('reftype',
                            domain.PK_TYPE,
                            ForeignKey('doctype.id'))
        reftype = relationship('DocType', uselist=False,
                               foreign_keys=[reftype_id],)

    class NumericVar(DocVar):
        __tablename__ = 'numvar'
        id = Column(domain.PK_TYPE,
                    ForeignKey('docvar.id'),
                    primary_key=True)
        value = Column('value', domain.Numeric)

    class DocRec(domain.Base):
        __tablename__ = 'docrec'
        id = Column(domain.PK_TYPE,
                    ForeignKey('DocVar.id'),
                    primary_key=True)
        doc_id = Column('doc', domain.PK_TYPE,
                        ForeignKey('Doc.id'),
                        primary_key=True)
        doc = relationship('Doc', back_populates='records',
                           uselist=False,
                           foreign_keys=[doc_id])
        var = relationship('DocVar', uselist=False, foreign_keys=[id])

        @declared_attr
        def __mapper_args__(cls):
            args = {'polymorphic_identity': cls.__tablename__}
            if cls.__tablename__ == 'docrec':
                args['polymorphic_on'] = column_property(
                    select([DocVar.kind], DocVar.id == id))
            return args

    class RefRec(DocRec):
        __tablename__ = 'refrec'
        id = Column(domain.PK_TYPE,
                    ForeignKey('docrec.id'),
                    primary_key=True)
        doc_id = Column('doc', domain.PK_TYPE,
                        ForeignKey('docrec.id'),
                        primary_key=True)
        ref_id = Column('ref', domain.PK_TYPE,
                        ForeignKey('doc.id'))
        ref = relationship('Doc', uselist=False, foreign_keys=['ref_id'])

    class NumRec(DocRec):
        __tablename__ = 'numrec'
        value = Column(domain.Numeric)

    domain.add_model('Person', Person, Person.id)
    domain.add_model('Doc', Doc, Doc.id)
    domain.add_model('DocType', DocType, DocType.id)
    domain.add_model('DocVar', DocVar, DocVar.id)
    domain.add_model('RefVar', ReferentialVar, ReferentialVar.id)
    domain.add_model('NumVar', NumericVar, NumericVar.id)
    domain.add_model('RefRec', RefRec, (RefRec.id, RefRec.doc_id))
    domain.add_model('NumRec', NumRec, NumRec.id)
    return domain
