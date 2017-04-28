from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal

from events.models import Attendance, Event
from reminders.models import Prompt
from reminders import tasks

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Attendance)
def attendance_prompts_schedule(sender, **kwargs):
    attendance = kwargs['instance']
    logger.info('attendance_prompts_schedule: %s' % attendance)
    tasks.schedule_event_prompts(attendance)


@receiver(post_delete, sender=Attendance)
def attendance_prompts_clear(sender, **kwargs):
    attendance = kwargs['instance']
    logger.info('attendance_prompts_clear: %s' % attendance)
    tasks.schedule_clear_prompts(attendance.id)


@receiver(post_save, sender=Event)
def event_prompts_reset(sender, **kwargs):
    event = kwargs['instance']
    logger.info('attendance_prompts_reset: %s' % event)
    for a in event.attendance_set.all():
        a.save() # to trigger attendance_prompts_schedule

@receiver(post_save, sender=Prompt)
def update_prompts(sender, **kwargs):
    prompt = kwargs['instance']
    logger.info('update_prompts: %s' % prompt)
    for e in Event.objects.filter(Q(prompt_before=prompt) | Q(prompt_after=prompt)):
        e.save() # to trigger event_prompts_reset
