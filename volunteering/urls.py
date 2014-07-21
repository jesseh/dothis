from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^import/$', 'volunteering.views.importer', name='import'),
    url(r'^volunteering/$', TemplateView.as_view(template_name='volunteering/claim.html')),
    url(r'^call_list/$', TemplateView.as_view(template_name='volunteering/call_list.html')),
)
