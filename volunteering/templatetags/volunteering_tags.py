from datetime import datetime
from django import template

from volunteering.models import Assignment

register = template.Library()


@register.inclusion_tag('volunteering/tags/event_report.html')
def event_report(assignment_or_event):
    if isinstance(assignment_or_event, Assignment):
        event = assignment_or_event.duty.event
    else:
        event = assignment_or_event

    return {'event': event,
            'generated_datetime': datetime.now(), }


@register.inclusion_tag('volunteering/tags/volunteered_for.html')
def volunteered_for(volunteer):
    return {'volunteer': volunteer}


@register.inclusion_tag('volunteering/tags/assignment_detail.html')
def assignment_detail(assignment):
    return {'assignment': assignment}
