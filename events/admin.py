# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Event, Participant

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'starts_at', 'ends_at')

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')


admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)