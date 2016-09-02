# coding:utf8

"""
需要序列化的类
"""

import json, time
from django.core.exceptions import ObjectDoesNotExist

import models


class ClientHandler(object):
    """
    客户端处理类
    """

    def __init__(self, client_id):
        self.client_id = client_id
        self.client_configs = {
            "services": {}
        }

    def fetch_configs(self):
        """
        获取配置信息
        :return:
        """
        try:
            host_obj = models.Host.objects.get(id=self.client_id)
            template_list = list(host_obj.templates.select_related())

            for host_group in host_obj.host_groups.select_related():
                template_list.extend(host_group.templates.select_related())
            print(template_list)
            for template in template_list:
                # print(template.services.select_related())

                for service in template.services.select_related():  # loop each service
                    print(service)
                    self.client_configs['services'][service.name] = [service.plugin_name, service.interval]
        except ObjectDoesNotExist, e:
            print(e)

        return self.client_configs


def get_host_triggers(host_obj):
    """
    获取主机的触发器列表
    :param host_obj:
    :return:
    """
    # host_obj = models.Host.objects.get(id=2)
    triggers = []
    for template in host_obj.templates.select_related():
        triggers.extend(template.triggers.select_related())
    for group in host_obj.host_groups.select_related():
        for template in group.templates.select_related():
            triggers.extend(template.triggers.select_related())

    return set(triggers)


class StatusSerializer(object):
    """
    主机状态
    """

    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    def by_hosts(self):
        """
        序列化所有的主机
        :return:
        """
        host_obj_list = models.Host.objects.all()
        host_data_list = []
        for host in host_obj_list:
            host_data_list.append(self.single_host_info(host))

        return host_data_list

    def single_host_info(self, host):
        """
        序列化单个主机的信息
        :param host:
        :return:
        """
        data = {
            'id': host.id,
            'name': host.name,
            'ip_addr': host.ip_addr,
            'status': host.status,
            'uptime': None,
            'last_update': None,
            'total_services': None,
            'ok_nums': None,
        }

        uptime = self.get_host_uptime(host)
        self.get_triggers(host)
        if uptime:
            print('uptime:', uptime)
            data['uptime'] = uptime[0]['uptime']
            data['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uptime[1]))
        data['triggers'] = self.get_triggers(host)

        return data

    def get_host_uptime(self, host):
        """
        获取主机最后一次更新时间
        :param host:
        :return:
        """
        redis_key = 'StatusData_%s_uptime_latest' % host.id
        last_data_point = self.redis_conn.lrange(redis_key, -1, -1)
        if last_data_point:
            last_data_point, last_update = json.loads(last_data_point[0])
            return last_data_point, last_update
        return None

    def get_triggers(self, host):
        """
        获取主机的触发器列表
        :param host:
        :return: None / trigger_dic
        """
        trigger_keys = self.redis_conn.keys("host_%s_trigger_*" % host.id)
        # 触发器的报警级别
        trigger_dic = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }
        if trigger_keys:
            for trigger_key in trigger_keys:
                trigger_data = self.redis_conn.get(trigger_key)
                if trigger_key.endswith("None"):
                    trigger_dic[4].append(json.loads(trigger_data))
                else:
                    trigger_id = trigger_key.split('_')[-1]
                    trigger_obj = models.Trigger.objects.get(id=trigger_id)
                    trigger_dic[trigger_obj.severity].append(json.loads(trigger_data))

        return trigger_dic


class TriggersView(object):
    def __init__(self, request, redis):
        self.request = request
        self.redis = redis

    def fetch_related_filters(self):
        by_host_id = self.request.GET.get('by_host_id')
        print('---host id:', by_host_id)
        # by_host_id = self.request.GET.get('by_host_id')
        host_obj = models.Host.objects.get(id=by_host_id)
        trigger_dic = {}
        if by_host_id:
            trigger_match_keys = "host_%s_trigger_*" % by_host_id
            trigger_keys = self.redis.keys(trigger_match_keys)
            print(trigger_keys)
            for key in trigger_keys:
                data = json.loads(self.redis.get(key))
                if data.get('trigger_id'):
                    trigger_obj = models.Trigger.objects.get(id=data.get('trigger_id'))
                    data['trigger_obj'] = trigger_obj
                data['host_obj'] = host_obj
                trigger_dic[key] = data

        return trigger_dic
