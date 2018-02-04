import os
from eve_sqlalchemy.config import DomainConfig, ResourceConfig

from racings import domain

SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_PATH = os.path.join(os.getcwd(), 'racings.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
DEBUG = True
RESOURCE_METHODS = ['GET', 'POST']

import os

DOMAIN = DomainConfig({
    k: ResourceConfig(v) for k, v in domain.EXPOSED.items()
}).render()
