# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import bulk_admin

from .models import Event, Participant, Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1 # just show one row by default

class ParticipantAdmin(bulk_admin.BulkModelAdmin):
    list_display = ('name', 'phone', 'email')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_starts_at', 'get_ends_at')
    inlines = (AttendanceInline,)


admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)