from datetime import datetime
from django import template

register = template.Library()


@register.inclusion_tag('volunteering/tags/event_report.html')
def event_report(event):
    """Full detail of duties and volunteers assigned to an event."""
    return {'event': event,
            'generated_datetime': datetime.now(), }


@register.inclusion_tag('volunteering/tags/volunteered_for.html')
def volunteered_for(volunteer):
    """List of assignments for which a volunteer has volunteered."""
    return {'volunteer': volunteer}


@register.inclusion_tag('volunteering/tags/assignment_detail.html')
def assignment_detail(assignment):
    """Details of an assignment including what, where and when."""
    return {'assignment': assignment}


@register.inclusion_tag('volunteering/tags/duty_volunteers.html')
def duty_volunteers(duty):
    """List of the names of volunteers who are assigned to a duty."""
    return {'duty': duty}
