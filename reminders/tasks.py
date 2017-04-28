from django_q.models import Schedule
import arrow
import random

def schedule_event_prompts(attendance):
    event = attendance.event
    
    # remove any existing prompts    
    schedule_clear_prompts(attendance)
    
    # render from template
    message_before = event.prompt_before.render(attendance)
    message_after = event.prompt_after.render(attendance)

    # schedule send_message task
    first_prompt_schedule = Schedule(func='messages.tasks.send_message',
            name='%s-prompt' % attendance.id,
            args=(attendance.participant.phone.as_e164, message_before),
        )
    second_prompt_schedule = Schedule(func='messages.tasks.send_message',
            name='%s-prompt' % attendance.id,
            args=(attendance.participant.phone.as_e164, message_after),
        )

    # set prompt send time in event timezone, with offset
    event_start = arrow.get(event.starts_at, event.time_zone)
    first_prompt_schedule.next_run = event_start.replace(minutes=+event.prompt_before.minutes_offset).to('utc').datetime
    first_prompt_schedule.repeats = 0
    
    event_end = arrow.get(event.ends_at, event.time_zone)
    second_prompt_schedule.next_run = event_end.replace(minutes=+event.prompt_after.minutes_offset).to('utc').datetime
    second_prompt_schedule.repeats = 0

    first_prompt_schedule.save()
    second_prompt_schedule.save()


def schedule_clear_prompts(attendance):
    # check for existing scheduled prompts
    s = Schedule.objects.filter(func='messages.tasks.send_message', name='%s-prompt' % attendance)
    s.delete()
