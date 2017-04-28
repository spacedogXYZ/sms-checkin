from .common import *
import dj_database_url

DEBUG = False

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
SECRET_KEY = os.environ.get('SECRET_KEY')

REQUIRED_KEYS = ['SECRET_KEY','TWILIO_ACCOUNT_SID','TWILIO_AUTH_TOKEN','TWILIO_MESSAGING_SID']
for key in REQUIRED_KEYS:
    if not key in os.environ:
        raise AttributeError('Please define %s in os.environ' % key)

# django-redis cache and broker
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "DB": 0,
        }
    }
}
Q_CLUSTER = {
    'name': 'DjangoQ-Redis',
    'workers': 4,
    'timeout': 90,
    'django_redis': 'default',
    'catch_up': False  # do not replay missed schedules past
}


INTERNAL_IPS = ['127.0.0.1', ]
CORS_ORIGIN_WHITELIST = (
    'localhost:4000',
)

if 'SENTRY_DSN' in os.environ:
    import raven
    INSTALLED_APPS += ('raven.contrib.django.raven_compat', )
    RAVEN_CONFIG = { 'dsn': os.environ.get('SENTRY_DSN') }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}