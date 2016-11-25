# coding:utf-8

import json

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from CrazyMonitor_v1 import settings
from monitor import graphs
from monitor import models
from monitor import serializer
from serializer import ClientHandler
from backends import data_optimization, redis_conn



def hosts(request):
    """
    获取主机群组
    """
    host_list = models.Host.objects.all()
    if (host_list):
        data = list(host_list)
        return HttpResponse(json.dumps(data))

    return HttpResponse(json.dumps({"stat": "OK"}))