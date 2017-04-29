from integrations.affinity import Affinity

import logging
logger = logging.getLogger(__name__)

def sync_event_from_affinity(event):
    """ Gets fields from Affinity API, saves them locally """
    affinity_client = Affinity()
    affinity_event = affinity_client.get('/events/%s.json' % event.crm_id).get('data', {})
    #NB fields mismatch
    event.title = affinity_event.get('title') 
    event.host_name = affinity_event.get('name')
    event.location = affinity_event.get('location', {}).get('venue')
    event.save()

    affinity_attendees = affinity_client.get_event_attendances(event.crm_id)
    for attendee in affinity_attendees:
        person = attendee.get('attributes', {}).get('person', {})
        attendee_name = u"%s %s" % (person.get('given-name'), person.get('family-name')) 
        attendee_email = person.get('primary-email-address')
        attendee_phone = person.get('primary-phone-number')

        # find attendee in set, using email as key (least likely to be formatted differently)
        local_instance = event.attendance_set.filter(email=attendee_email)
        if not local_instance:
            local_instance = Participant()

        data = {}
        # only sync fields if we got data for them
        if attendee_name:
            data['name'] = attendee_name
        if attendee_email:
            data['email'] = attendee_email
        if attendee_phone:
            data['phone'] = attendee_phone
        local_instance.update(**data)
        event.attendee_set.add(local_instance)
    event.save()

def sync_attendance_to_affinity(attendance):
    affinity_client = Affinity()
    if not attendance.crm_id:
        affinity_attendees = affinity_client.get_event_attendances(attendance.crm_id)
        for attendee in affinity_attendees:
            if attendee['attributes']['person']['primary-email-address'] == attendance.participant.email:
                attendance.crm_id = attendee['id']

    affinity_client.put('/api/v1/events/%s/attendance/%s' % (attendance.event.crm_id, attendance.crm_id),
        {'attended': attendance.confirmed})
    attendance.save()
