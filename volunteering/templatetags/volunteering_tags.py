from django import template

register = template.Library()


@register.inclusion_tag('volunteering/event_report.html')
def event_report(assignment):
    return {'event': assignment.duty.event}
