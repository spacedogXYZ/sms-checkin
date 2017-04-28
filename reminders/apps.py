# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class RemindersConfig(AppConfig):
    name = 'reminders'

    def ready(self):
        import reminders.signals
