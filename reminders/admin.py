# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from .models import Prompt, Message

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class PromptAdmin(admin.ModelAdmin):
    list_display = ('name', 'minutes_offset', 'message')


class MessageForm(forms.ModelForm):
    # read-only form for admin
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Message
        exclude = []


class MessageAdmin(admin.ModelAdmin):
    list_display = ('to_participant', 'body', 'sent_at', 'status')
    form = MessageForm

    # remove add/change/delete permissions from admin
    # because we will only create Message objects via scheduled jobs
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return True # so we can see the messages, but all fields are readonly
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Prompt, PromptAdmin)
admin.site.register(Message, MessageAdmin)