import importlib
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import attr


@attr.s
class Domain:
    """This class is a place to specify all the project-level
    conventions on how to compose data models.
    A model is uniquely identified by its name. The structure of the data
    is described in the relational model using the SQLAlchemy.
    `Domain` maps names of models to SQLA orm models.
     An SQLA model can be retrieved by its name either using getattr (e.g.
     `Domain.User`) or as an item of `Domain.models`. A model can be added
     using `Domain.add_model`.
    `Domain.PK_TYPE` is the artificial primary key sqla type used by default.
    `Domain` also contains as an element a map `PK` which maps a model name
    into its PK columns.

    How to define a new model in a separate package
    ---

    Write a factory method `add_models(domain)`
    in the `youpackage.domain` module.
    This method shall generate new sqla.orm classes
    inheriting from `domain.Base`"""

    PK_TYPE = attr.ib(default=sa.Integer)
    PK = attr.ib(default=attr.Factory(dict))
    Numeric = attr.ib(default=attr.Factory(lambda: sa.Numeric(10, 4)))
    models = attr.ib(default=attr.Factory(dict))
    Base = attr.ib(default=attr.Factory(declarative_base))
    common_columns = attr.ib(default=attr.Factory(list))

    def __getattr__(self, attr):
        try:
            return self.models[attr]
        except KeyError:
            pass
        raise AttributeError(attr)

    def add_model(self, name, model, pk):
        overwriting = (name in self.models
                       and (self.models[name] != model
                            or self.PK[name] != pk))
        if overwriting:
            raise Exception('Model {} has already been registered'
                            .format(name))
        self.models[name] = model
        self.PK[name] = pk

    def use_package(self, package):
        importlib.import_module('{}.model'.format(package)).add_models(self)
