# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twilio.rest import Client

from django.shortcuts import render

def send_message(to_number, body):
    status = message = client.messages.create(
        body=body,
        to=to_number,
        from_=settings.TWILIO_MESSAGING_SID,
    )
    return status