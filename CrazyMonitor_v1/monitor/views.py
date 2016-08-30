# coding:utf8

import json

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from CrazyMonitor_v1 import settings
from monitor import models
from monitor.backends import data_processing
from serializer import ClientHandler, get_host_triggers
from backends import data_optimization, redis_conn

# redis connection
REDIS_CONN = redis_conn.redis_conn(settings)


def client_configs(request, client_id):
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()
    if config:
        return HttpResponse(json.dumps(config))
    else:
        return HttpResponse(json.dumps('{"status":"ERROR_CONFIG_NOT_FOUND"}'))


@csrf_exempt
def service_data_report(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])
        print("Client update data:", data)
        client_id = request.POST.get('client_id')
        service_name = request.POST.get('service_name')
        data_save_obj = data_optimization.DataStore(client_id, service_name, data, REDIS_CONN)

        # start triggers
        host_obj = models.Host.objects.get(id=client_id)
        service_triggers = get_host_triggers(host_obj)

        trigger_handler = data_processing.DataHandler(settings, connect_redis=False)
        for trigger in service_triggers:
            trigger_handler.load_service_data_and_calulating(host_obj, trigger, REDIS_CONN)
        print("service trigger::", service_triggers)

        # 更新主机存活状态
        # host_alive_key = "HostAliveFlag_%s" % client_id
        # REDIS_OBJ.set(host_alive_key,time.time())
    return HttpResponse(json.dumps('{"status":"OK"}'))
