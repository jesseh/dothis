from datetime import datetime
from django import template

register = template.Library()


@register.inclusion_tag('volunteering/tags/event_report.html')
def event_report(event):
    return {'event': event,
            'generated_datetime': datetime.now(), }


@register.inclusion_tag('volunteering/tags/volunteered_for.html')
def volunteered_for(volunteer):
    return {'volunteer': volunteer}


@register.inclusion_tag('volunteering/tags/assignment_detail.html')
def assignment_detail(assignment):
    return {'assignment': assignment}


@register.inclusion_tag('volunteering/tags/duty_volunteers.html')
def duty_volunteers(duty):
    return {'duty': duty}
