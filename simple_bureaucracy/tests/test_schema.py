from simple_bureaucracy.model import add_models


def test_schema():
    import sqlalchemy as sa
    from modular_sqla import Domain
    eng = sa.create_engine('sqlite:///')
    domain = Domain()
    add_models(domain)
    domain.Base.metadata.create_all(eng)
    domain.Person._sa_class_manager.mapper.iterate_properties
