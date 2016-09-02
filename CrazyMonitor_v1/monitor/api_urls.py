# coding:utf8

from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    # client get config
    url(r'client/config/(\d)/$', views.client_configs),
    # client commit data
    url(r'client/service/report/$', views.service_data_report),
    url(r'hosts/status/$', views.hosts_status, name="get_hosts_status"),
    url(r'graphs/$', views.graphs_gerator, name='get_graphs'),
)
