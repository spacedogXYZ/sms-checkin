# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from twilio import twiml

from django.shortcuts import render

from events.models import Participant
from requests import decompose
from parsers import is_yes, is_no, is_number

def message(request):
    r = twiml.Response()
    twilio_request = decompose(request)

    # get participant from phone number
    try:
        participant = Partipant.objects.get(phone=twilio_request.from_)
    except Participant.DoesNotExist:
        r.message("You do not seem to be signed up to use this system. Please contact info@affinity.works")
        return r

    if not participant.attendance_set:
        r.message("Sorry, you do not seem to be invited to any upcoming events.")
        return r

    if not participant.confirmed:
        # check in
        if is_yes(twilio_request.body):
            participant.confirmed = True
            participant.save()
            r.message("Thanks for checking in to %s!" % participant.event.name)
            return r
        elif is_no(twilio_request.body):
            participant.confirmed = False
            participant.save()
            r.message("Sorry you won't be able to make it to %s." % participant.event.name)
            return r
        else:
            r.message("Please reply with just Y or N.")
            return r

    else:
        # rate event
        if is_number(twilio_request.body):
            try:
                attendance = participant.attending_events()[0]
            except IndexError:
                r.message("Sorry, we could not find the event you were attending.")
                return r
            attendance.rating = int(twilio_request.body)
            attendance.save()
            r.message("Thanks for rating the event.")
            return r
        else:
            r.message("Please reply with a number 1-3 rating the event.")
            return r

    return r