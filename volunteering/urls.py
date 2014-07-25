from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import SummaryView, DutyView

CAMPAIGN_SLUG = "(?P<campaign_slug>[-\w]+)"
DUTY_SLUG = "(?P<duty_slug>[-\w]+)"
VOLUNTEER_SLUG = "(?P<volunteer_slug>\w\w\w\w-\w\w\w\w)"

urlpatterns = patterns('',
    url(r'^%s/$' % VOLUNTEER_SLUG, SummaryView.as_view(), name='summary'),

    url(r'^%s/%s/%s/$' % (VOLUNTEER_SLUG, CAMPAIGN_SLUG, DUTY_SLUG), DutyView.as_view(),
        name='duty'),

    url(r'^import/$', 'volunteering.views.importer', name='import'),

    url(r'^call_list/$',
        TemplateView.as_view(template_name='volunteering/call_list.html')),
)