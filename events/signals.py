from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

import django_q

from models import Event
from tasks import sync_event_from_affinity

import logging
logger = logging.getLogger(__name__)

sync_event_from_affinity = Signal()

@receiver(sync_event_from_affinity)
def event_sync_from_affinity(sender, **kwargs):
    event = kwargs['instance']
    logger.info('event_sync_from_affinity: %s' % event.id)
    # call the affinity task async, so we can respond immediately in the admin
    django_q.tasks.async('events.tasks.sync_event_from_affinity', event)

