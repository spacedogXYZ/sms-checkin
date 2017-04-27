# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse

from django.db import models
from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField

from reminders.models import Prompt

class Event(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, null=True)
    host_name = models.CharField(max_length=150, null=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    time_zone = TimeZoneField(default='US/Pacific')

    created = models.DateTimeField(auto_now_add=True)

    prompt_before = models.ForeignKey(Prompt, related_name='+', null=True)
    prompt_after = models.ForeignKey(Prompt, related_name='+', null=True)

    def __str__(self):
        return 'Event #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('view_event', args=[str(self.id)])


class Participant(models.Model):
    name = models.CharField(max_length=150)
    phone = PhoneNumberField()
    email = models.EmailField()

    event = models.ForeignKey(Event)
    
    def __str__(self):
        return 'Participant #{0} - {1}'.format(self.pk, self.name)