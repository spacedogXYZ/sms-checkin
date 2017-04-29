# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from twilio.rest import Client

import logging
logger = logging.getLogger(__name__)

def send_message(to_number, body):
    twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    logger.info('send_message to %s: %s' % (to_number, body))
    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO_MESSAGING_SID,
    )
    return message.status