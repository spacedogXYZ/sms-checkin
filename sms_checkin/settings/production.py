from .common import *
import dj_database_url

DEBUG = False

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ.get('SECRET_KEY')
else:
    raise AttributeError('Please define SECRET_KEY in os.environ')