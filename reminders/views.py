# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

from django.shortcuts import render

from events.models import Participant
from messages.decorators import twilio_view
from messages.requests import decompose
from messages.parsers import is_yes, is_no, is_number, is_reset


@twilio_view
def incoming_message(request):
    r = MessagingResponse()
    twilio_request = decompose(request)
    message = twilio_request.body

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
        if is_yes(message):
            attendance.confirmed = True
            attendance.save()
            r.message("Thanks for checking in to %s!" % attendance.event.name)
            return r
        elif is_no(message):
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
            if is_number(message):
                attendance.rating = int(message)
                attendance.save()
                r.message("Thanks for rating the event.")
                return r
            else:
                r.message("Please reply with a number 1-3 rating the event.")
                return r
        else:
            if is_reset(message):
                attendance.rating = None
                attendance.save()
                r.message("Your rating is reset. Please reply with a number 1-3 rating the event.")
                return r
            else:
                r.message("We're all done. If you'd like to reset your event rating, reply RESET.")
                return r
    return r