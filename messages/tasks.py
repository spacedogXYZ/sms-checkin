# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from twilio.rest import Client

from reminders.models import Message
from events.models import Participant

import logging
logger = logging.getLogger(__name__)

def send_message(to_number, body):
    twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    logger.info('send_message to %s: %s' % (to_number, body))
    twilio_message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO_MESSAGING_SID,
    )

    # also save to our database
    to_participant = Participant.objects.get(phone=to_number)
    message = Message(body=body, to_participant=to_participant)
    message.sent_at = datetime.now()
    message.status = twilio_message.status
    message.save()

    return message.status == 'accepted'