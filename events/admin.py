# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import admin, messages

from .models import Event, Participant, Attendance
from .signals import sync_event_from_affinity

class EventAdmin(admin.ModelAdmin):
    list_display = ('crm_id', 'name', 'get_starts_at', 'get_ends_at', 'sync_event')
    fieldsets = (
        ('Main', {
            'fields': ('name', 'crm_id',)
        }),
        ('Time', {
            'fields': ('time_zone', 'starts_at', 'ends_at')
        }),
        ('Message Prompts', {
            'fields': ('prompt_before', 'prompt_after')
        }),
        ('Synced from Affinity', {
            'classes': ('collapse',),
            'fields': ('host_name', 'location'),
        }),
    )

    # add a custom button to the admin list
    def sync_event(self, obj):
        return format_html(
            '<a class="button" href="{}">Sync</a>',
            reverse('admin:start-event-sync', args=[obj.pk]),
        )
    sync_event.short_description = "Actions"

    def start_event_sync(self, request, *args, **kwargs):
        instance = Event.objects.get(id=kwargs['event_id'])
        sync_event_from_affinity.send(Event, instance=instance)

        messages.add_message(request, messages.INFO, 'Started sync for event "%s".' % instance)
        return redirect('/admin/events/event')

    def get_urls(self):
        urls = super(EventAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<event_id>.+)/sync/$',
                self.admin_site.admin_view(self.start_event_sync),
                name='start-event-sync',
            )
        ]
        return custom_urls + urls


class AttendanceAdmin(admin.TabularInline):
    model = Attendance
    extra = 1 # just show one row by default

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    inlines = (AttendanceAdmin,)

admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)