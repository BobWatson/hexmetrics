#!flask/bin/python

import sys, os

sys.path.append(os.path.join(os.getcwd(), os.pardir))

from migrate.versioning import api
from hex.config import SQLALCHEMY_DATABASE_URI
from hex.config import SQLALCHEMY_MIGRATE_REPO
from hex.main import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))