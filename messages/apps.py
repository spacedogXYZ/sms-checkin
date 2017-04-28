# foo/apps.py

from django.apps import AppConfig

class SMSConfig(AppConfig):
    name = 'messages'
    label = 'sms_checkin.messages'