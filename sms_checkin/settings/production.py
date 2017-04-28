from .common import *
import dj_database_url

DEBUG = False

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
SECRET_KEY = os.environ.get('SECRET_KEY')

REQUIRED_KEYS = ['SECRET_KEY','TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','TWILIO_MESSAGING_SID']
for key in REQUIRED_KEYS:
    if not key in os.environ:
        raise AttributeError('Please define %s in os.environ' % key)
    