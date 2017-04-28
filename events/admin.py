# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Event, Participant, Attendance

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_starts_at', 'get_ends_at')

class AttendanceAdmin(admin.TabularInline):
    model = Attendance
    extra = 1 # just show one row by default

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    inlines = (AttendanceAdmin,)

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)