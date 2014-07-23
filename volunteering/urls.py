from django.conf.urls import patterns, url
from django.views.generic import TemplateView

CAMPAIGN_SLUG = "(?P<campaign_slug>[-\w]+)"
DUTY_SLUG = "(?P<duty_slug>[-\w]+)"
VOLUNTEER_SLUG = "(?P<volunteer_slug>\w\w\w\w-\w\w\w\w)"

urlpatterns = patterns('',
    url(r'^%s/$' % VOLUNTEER_SLUG,
        TemplateView.as_view(template_name='volunteering/summary.html')),
    url(r'^%s/%s/%s/$' % (VOLUNTEER_SLUG, CAMPAIGN_SLUG, DUTY_SLUG),
        TemplateView.as_view(template_name='volunteering/opportunity.html')),
    url(r'^import/$', 'volunteering.views.importer', name='import'),
    url(r'^call_list/$',
        TemplateView.as_view(template_name='volunteering/call_list.html')),
)
