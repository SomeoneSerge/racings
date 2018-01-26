from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from racings import domain

DOMAIN = DomainConfig({
    k: ResourceConfig(v) for k, v in domain.EXPOSED.items()
}).render()
