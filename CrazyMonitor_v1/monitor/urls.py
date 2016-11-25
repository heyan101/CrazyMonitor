# coding:utf8

from django.conf.urls import url

import views, api

urlpatterns = [
    url(r'^$', views.console),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^triggers/$', views.triggers, name='triggers'),
    url(r'hosts/$', api.hosts, name='hosts'),
    url(r'hosts/(\d+)/$', views.host_detail, name='host_detail'),
    url(r'trigger_list/$', views.trigger_list, name='trigger_list'),
]
