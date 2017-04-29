# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

from django.shortcuts import render

from events.models import Participant
from messages.decorators import twilio_view
from messages.requests import decompose
from messages.parsers import ParseMessage


@twilio_view
def incoming_message(request):
    r = MessagingResponse()
    twilio_request = decompose(request)
    message = ParseMessage(twilio_request.body)

    # get participant from phone number
    try:
        participant = Participant.objects.get(phone=twilio_request.from_)
    except Participant.DoesNotExist:
        r.message("You do not seem to be signed up to use this system. Please contact info@affinity.works")
        return r

    if not participant.attending:
        r.message("Sorry, you do not seem to be attending any upcoming events.")
        return r
    else:
        attendance = participant.attending[0]

    if not attendance.confirmed:
        # check in
        if message.is_yes():
            attendance.confirmed = True
            attendance.save()
            r.message("Thanks for checking in to %s!" % attendance.event.name)
            return r
        elif message.is_no():
            attendance.confirmed = False
            attendance.save()
            r.message("Sorry you won't be able to make it to %s." % attendance.event.name)
            return r
        else:
            r.message("Please reply with just Y or N.")
            return r

    else:
        if not attendance.rating:
            # rate event
            if message.is_number():
                attendance.rating = int(message.body)
                attendance.save()
                r.message("Thanks for rating the event.")
                return r
            else:
                r.message("Please reply with a number 1-3 rating the event.")
                return r
        else:
            if message.is_reset():
                attendance.rating = None
                attendance.save()
                r.message("Your rating is reset. Please reply with a number 1-3 rating the event.")
                return r
            else:
                r.message("We're all done. If you'd like to reset your event rating, reply RESET.")
                return r
    return r