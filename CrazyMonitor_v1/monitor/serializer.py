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
    #host_obj = models.Host.objects.get(id=2)
    triggers = []
    for template in host_obj.templates.select_related():
        triggers.extend(template.triggers.select_related())
    for group in host_obj.host_groups.select_related():
        for template in group.templates.select_related():
            triggers.extend(template.triggers.select_related())

    return set(triggers)
