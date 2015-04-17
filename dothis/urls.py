from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import TemplateView

from djrill.views import (DjrillIndexView, DjrillSendersListView,
                          DjrillTagListView,
                          DjrillUrlListView)


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(
        template_name='dothis/home.html'), name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # From Djrill
    url("admin/email/senders/",
        admin.site.admin_view(DjrillSendersListView.as_view()),
        name="djrill_senders"),
    url("admin/email/status/",
        admin.site.admin_view(DjrillIndexView.as_view()),
        name="djrill_status",
        ),
    url("admin/email/tags/",
        admin.site.admin_view(DjrillTagListView.as_view()),
        name="djrill_tags"),
    url("admin/email/urls/",
        admin.site.admin_view(DjrillUrlListView.as_view()),
        name="djrill_urls"),

    url(r'^volunteering/', include('volunteering.urls',
                                   namespace='volunteering')),
    url(r'^styles/', include('foundation.urls')),
    url(r'^robots\.txt$', lambda r: HttpResponse(
        content="User-agent: *\nDisallow: /*",
        content_type="text/plain")),
)

