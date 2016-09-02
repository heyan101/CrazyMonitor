# coding:utf8

import time

from monitor.backends import redis_conn


class DataHandler(object):
    """
    数据处理
    """

    def __init__(self, django_settings, connect_reids=True):
        self.django_settings = django_settings
        self.poll_interval = 0.5
        self.config_update_interval = 120
        self.config_lase_loading_time = time.time()
        self.global_monitor_dic = {}
        self.exit_flag = False
        if connect_reids:
            self.redis = redis_conn.redis_conn(django_settings)

    def load_service_data_and_calulating(self, host_obj, trigger, REDIS_CONN):
        """
        fetching out service data from redis db and calculate according to each serivce's trigger configuration
        :param host_obj:
        :param trigger_obj:
        :param REDIS_CONN: #从外面调用此函数时需传入redis_obj,以减少重复连接
        :return:
        """

        self.redis = REDIS_CONN
        calc_sub_res_list = []  # 先把每个expression的结果算出来放在这个列表里,最后再统一计算这个列表
        positive_expressions = []
        expression_res_string = ''
