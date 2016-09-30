# coding:utf8

from django.conf.urls import url

import views

urlpatterns = [
    url(r'report', views.service_data_report),
]
