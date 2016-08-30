from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from monitor import api_urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include('monitor.api_urls')),
    url(r'^monitor/', include('monitor.urls'))
)

