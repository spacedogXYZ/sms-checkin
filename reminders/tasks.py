from django_q.models import Schedule
from django.utils.timezone import get_current_timezone
import arrow
import random

import logging
logger = logging.getLogger(__name__)

def schedule_attendance_prompts(attendance):
    event = attendance.event

    logger.info('schedule_attendance_prompts: %s' % attendance.id)
    
    # remove any existing prompts for this attendance
    schedule_clear_prompts(attendance)
    
    # render from template
    message_before = event.prompt_before.render(attendance)
    message_after = event.prompt_after.render(attendance)
    logger.info('message_before: %s' % message_before)
    logger.info('message_after: %s' % message_after)

    # schedule send_message task
    first_prompt_schedule = Schedule(func='messages.tasks.send_message',
            name='%s-prompt' % attendance.id,
            args=(attendance.participant.phone.as_e164, message_before),
        )
    second_prompt_schedule = Schedule(func='messages.tasks.send_message',
            name='%s-prompt' % attendance.id,
            args=(attendance.participant.phone.as_e164, message_after),
        )

    # set prompt send times, with minutes offset, in UTC
    first_prompt_next_run = arrow.get(event.get_starts_at()).replace(minutes=+event.prompt_before.minutes_offset)
    first_prompt_schedule.next_run = first_prompt_next_run.to(get_current_timezone()).datetime
    first_prompt_schedule.repeats = 0
    logger.info('first_prompt_scheduled at: %s' % first_prompt_schedule.next_run)
    
    second_prompt_next_run = arrow.get(event.get_ends_at()).replace(minutes=+event.prompt_after.minutes_offset)
    second_prompt_schedule.next_run = second_prompt_next_run.to(get_current_timezone()).datetime
    second_prompt_schedule.repeats = 0
    logger.info('second_prompt_schedule at: %s' % second_prompt_schedule.next_run)

    first_prompt_schedule.save()
    second_prompt_schedule.save()


def schedule_clear_prompts(attendance):
    # check for existing scheduled prompts
    s = Schedule.objects.filter(func='messages.tasks.send_message', name='%s-prompt' % attendance.id)
    s.delete()
