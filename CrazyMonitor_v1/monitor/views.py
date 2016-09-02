# coding:utf8

import json

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from CrazyMonitor_v1 import settings
from monitor import graphs
from monitor import models
from monitor import serializer
from serializer import ClientHandler
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
        data_saveing_obj = data_optimization.DataStore(client_id, service_name, data, REDIS_CONN)

        # start triggers
        # host_obj = models.Host.objects.get(id=client_id)
        # service_triggers = get_host_triggers(host_obj)
        #
        # trigger_handler = data_processing.DataHandler(settings, connect_redis=False)
        # for trigger in service_triggers:
        #     trigger_handler.load_service_data_and_calulating(host_obj, trigger, REDIS_CONN)
        # print("service trigger::", service_triggers)

        # 更新主机存活状态
        # host_alive_key = "HostAliveFlag_%s" % client_id
        # REDIS_OBJ.set(host_alive_key,time.time())
    return HttpResponse(json.dumps('{"status":"OK"}'))


def hosts_status(request):
    # 获取序列化后的主机信息
    hosts_data_serializer = serializer.StatusSerializer(REDIS_CONN)
    hosts_data = hosts_data_serializer.by_hosts()

    return HttpResponse(json.dumps(hosts_data))


def graphs_gerator(request):
    """
    获取一台主机的所有数据
    :param request:
    :return:
    """
    graphs_generator = graphs.GraphGenerator2(REDIS_CONN)
    print("GET================================================", request.GET)
    graphs_data = graphs_generator.get_host_graph(request.GET.get('host_id'), request.GET.get('time_range'))

    return HttpResponse(json.dumps(graphs_data))


def index(request):
    return render(request, 'monitor/index.html')


def dashboard(request):
    return render(request, 'monitor/dashboard.html')


def triggers(request):
    return render(request, 'monitor/triggers.html')


def hosts(request):
    host_list = models.Host.objects.all()
    print("hosts:", host_list)
    return render(request, 'monitor/hosts.html', {'host_list': host_list})


def host_detail(request, host_id):
    host_obj = models.Host.objects.get(id=host_id)
    return render(request, 'monitor/host_detail.html', {'host_obj': host_obj})


def host_detail_old(request, host_id):
    host_obj = models.Host.objects.get(id=host_id)

    # config_obj = ClientHandler(host_obj.id)
    monitored_services = {
        "services": {},
        "sub_services": {}  # 存储一个服务有好几个独立子服务 的监控,比如网卡服务 有好几个网卡
    }

    template_list = list(host_obj.templates.select_related())

    for host_group in host_obj.host_groups.select_related():
        template_list.extend(host_group.templates.select_related())
    for template in template_list:

        for service in template.services.select_related():  # loop each service
            if not service.has_sub_service:
                monitored_services['services'][service.name] = [service.plugin_name, service.interval]
            else:
                monitored_services['sub_services'][service.name] = []

                # get last point from redis in order to acquire the sub-service-key
                last_data_point_key = "StatusData_%s_%s_latest" % (host_obj.id, service.name)
                last_point_from_redis = REDIS_CONN.lrange(last_data_point_key, -1, -1)[0]
                if last_point_from_redis:
                    data, data_save_time = json.loads(last_point_from_redis)
                    if data:
                        service_data_dic = data.get('data')
                        for serivce_key, val in service_data_dic.items():
                            monitored_services['sub_services'][service.name].append(serivce_key)

    return render(request, 'host_detail.html', {'host_obj': host_obj, 'monitored_services': monitored_services})


def graph_bak(request):
    # host_id = request.GET.get('host_id')
    # service_key = request.GET.get('service_key')
    graph_generator = graphs.GraphGenerator(request, REDIS_CONN)
    graph_data = graph_generator.get_graph_data()
    if graph_data:
        return HttpResponse(json.dumps(graph_data))


def trigger_list(request):
    trigger_handle_obj = serializer.TriggersView(request, REDIS_CONN)
    trigger_data = trigger_handle_obj.fetch_related_filters()

    return render(request, 'monitor/trigger_list.html', {'trigger_list': trigger_data})
