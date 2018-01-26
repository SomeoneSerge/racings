from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from racings import domain

SQLALCHEMY_DATABASE_URI = 'sqlite:///racings.db'

DOMAIN = DomainConfig({
    k: ResourceConfig(v) for k, v in domain.EXPOSED.items()
}).render()
