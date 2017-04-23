from django.conf.urls import url
from django.contrib import admin

from events.views import EventListView, EventDetailView

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='home'),
    url(r'^event/(?P<pk>[0-9]+)/$', EventDetailView.as_view(), name='view_event'),
    url(r'^admin/', admin.site.urls),
]
