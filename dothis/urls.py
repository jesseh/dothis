from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='dothis/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^volunteering/', include('volunteering.urls', namespace='volunteering')),
    url(r'^styles/', include('foundation.urls')),
)
