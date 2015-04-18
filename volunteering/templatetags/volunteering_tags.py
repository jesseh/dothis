from django import template

register = template.Library()


@register.inclusion_tag('results.html')
def event_report(assignment):
    return {'event': assignment.duty.event}
