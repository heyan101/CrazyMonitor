from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('monitor.api_urls')),
    url(r'^monitor/', include('monitor.urls')),
]

