import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = '0b7739988383e2b68b6e70326bc6e4c9'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://testusr:test@localhost:5432/dfastore'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')