from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='dothis/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^volunteering/', include('volunteering.urls',
                                   namespace='volunteering')),
    url(r'^styles/', include('foundation.urls')),
    url(r'^robots\.txt$', lambda r: HttpResponse(
        content="User-agent: *\nDisallow: /*",
        content_type="text/plain")),
)
