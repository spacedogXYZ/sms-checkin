"""
WSGI config for sms_checkin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sms_checkin.settings.development")
# can be overridden in os.environ

application = get_wsgi_application()

if os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[-1] == 'production':
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)