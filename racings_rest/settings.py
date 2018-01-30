from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from racings import domain

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///racings.db'
DEBUG = True
RESOURCE_METHODS = ['GET', 'POST']

DOMAIN = DomainConfig({
    k: ResourceConfig(v) for k, v in domain.EXPOSED.items()
}).render()
