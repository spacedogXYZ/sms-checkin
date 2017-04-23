# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Prompt(models.Model):
    minutes_offset = models.IntegerField()
    name = models.CharField(max_length=32)
    message = models.TextField()

    def __str__(self):
        return 'Prompt #{0} - {1}'.format(self.pk, self.name)

class Message(models.Model):
    to_participant = models.ForeignKey('events.Participant') # use string to avoid circular imports
    body = models.TextField()
    sent_at = models.DateTimeField()