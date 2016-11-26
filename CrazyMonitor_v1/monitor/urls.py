# coding:utf8

from django.conf.urls import url

import views, api

urlpatterns = [
    url(r'^getHostGroupList/$', api.getHostGroupList),
    # url(r'^$', views.console),
    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # url(r'^triggers/$', views.triggers, name='triggers'),
    # url(r'hosts/$', api.hosts, name='hosts'),
    # url(r'hosts/(\d+)/$', views.host_detail, name='host_detail'),
    # url(r'trigger_list/$', views.trigger_list, name='trigger_list'),

    # client get config
    url(r'client/config/(\d)/$', views.client_configs),
    # client commit data
    url(r'client/service/report/$', views.service_data_report),
    url(r'hosts/status/$', views.hosts_status, name="get_hosts_status"),
    url(r'graphs/$', views.graphs_gerator, name='get_graphs'),
]
