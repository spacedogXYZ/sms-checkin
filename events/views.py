# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic.list import ListView

from .models import Event

class EventListView(ListView):
    model = Event

class EventDetailView(DetailView):
    model = Event