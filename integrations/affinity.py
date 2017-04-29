import requests
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

class Affinity(object):
    def __init__(self, url_base=settings.AFFINITY_URL_BASE, token=settings.HTTP_OSDI_API_TOKEN):
        self.auth = {"HTTP_OSDI_API_TOKEN": token}
        self.url_base = url_base

    def get(self, url):
        r = requests.get(self.url_base+url, headers=self.auth)
        logger.debug('affinity.get: %s' % self.url_base+url)
        logger.debug('result: %s' % r.json())
        return r.json()

    def put(self, url, data):
        r = requests.put(self.url_base+url, data, headers=self.auth)
        logger.debug('affinity.put: %s, %s' % (self.url_base+url, data))
        logger.debug('result: %s' % r.json())
        return r.json()

    # convenience methods
    def get_event_attendances(self, event_id):
        return self.get('/events/%s/attendances.json' % event_id).get('data', [])

    def get_person(self, person_id):
        return self.get('/person/%s.json' % person_id).get('data', [])