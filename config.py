import os
CSRF_ENABLED = True
SECRET_KEY = 'send-us-a-patch'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'q.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

