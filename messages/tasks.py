# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twilio.rest import Client

from django.shortcuts import render
from django.conf import settings


def send_message(to_number, body):
    twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = twilio_client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO_MESSAGING_SID,
    )
    return message.status