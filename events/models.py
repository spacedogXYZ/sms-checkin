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

    @property
    def participants(self):
        return [a.participant for a in self.attendance_set.select_related('participant')]

    @property
    def confirmed(self):
        return self.attendance_set.filter(confirmed=True)


class Participant(models.Model):
    name = models.CharField(max_length=150)
    phone = PhoneNumberField()
    email = models.EmailField()

    event = models.ManyToManyField(Event, through='Attendance')
    
    def __str__(self):
        return 'Participant #{0} - {1}'.format(self.pk, self.name)

    @property
    def attending(self):
        return [a for a in self.attendance_set.select_related('event').order_by('event__ends_at')]

class Attendance(models.Model):
    participant = models.ForeignKey(Participant)
    event = models.ForeignKey(Event)
    confirmed = models.NullBooleanField(default=None, blank=True, null=True)
    rating = models.IntegerField(default=None, blank=True, null=True)

    class Meta:
        verbose_name_plural = "attending"