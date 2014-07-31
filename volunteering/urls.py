from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import SummaryView, AssignmentView

VOLUNTEER_SLUG = "(?P<volunteer_slug>\w\w\w\w-\w\w\w\w)"
DUTY_ID = "(?P<duty_id>\d+)"

urlpatterns = patterns('',
    url(r'^%s/$' % VOLUNTEER_SLUG, SummaryView.as_view(), name='summary'),

    url(r'^%s/%s/$' % (VOLUNTEER_SLUG, DUTY_ID),
        AssignmentView.as_view(),
        name='assignment'),

    url(r'^import/$', 'volunteering.views.importer', name='import'),

    url(r'^call_list/$',
        TemplateView.as_view(template_name='volunteering/call_list.html')),
)
