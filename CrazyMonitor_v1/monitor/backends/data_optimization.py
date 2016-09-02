# coding:utf8

"""
后台数据优化
"""
import copy
import json
import time

from CrazyMonitor_v1 import settings


class DataStore(object):
    """
    processing the client reported service data , do some data optimiaztion and save it into redis DB
    """

    def __init__(self, client_id, service_name, data, redis_conn):
        """
        :param client_id:
        :param service_name:
        :param data: the client reported service clean data
        :param redis_conn: redis connection
        """
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.redis_conn = redis_conn
        self.process_and_save()

    def process_and_save(self):
        """
        处理数据并保存到 Redis
        :param self:
        :return:
        """
        if self.data['status'] == 0:  # 服务端数据是有效的
            # 这里的 key = [latest, 10mins, 30mins, 60mins],data_series_val = [[0,600],[600,600],[1800,600],...]
            for key, data_series_val in settings.STATUS_DATA_OPTIMIZATION.items():
                # redis 中的表名
                data_series_key_in_redis = "StatusData_%s_%s_%s" % (self.client_id, self.service_name, key)
                # 获取表中最后一条数据
                last_point_from_redis = self.redis_conn.lrange(data_series_key_in_redis, -1, -1)
                if not last_point_from_redis:
                    '''
                    表中没有数据，将插入一条空的数据，里面只保存一个当前时间，这个时间的作用是待会数据优化的时候，去判断上次
                    保存数据的时间间隔
                    '''
                    self.redis_conn.rpush(data_series_key_in_redis, json.dumps([None, time.time()]))
                # 取出来的是保存数据的时间间隔，等于0 表示要保存的是实时数据，直接在 data 的最后面加上时间，然后写入 redis
                if data_series_val[0] == 0:
                    self.redis_conn.rpush(data_series_key_in_redis, json.dumps([self.data, time.time()]))
                else:  # 数据需要优化
                    # 取出最后一条数据， last_point_save_time 为上条数据保存的时间
                    last_point_data, last_point_save_time = \
                        json.loads(self.redis_conn.lrange(data_series_key_in_redis, -1, -1)[0])
                    # 达到数据点的更新间隔
                    if time.time() - last_point_save_time >= data_series_val[0]:
                        # 取出实时数据表中最近 n 秒的数据，放入 data_set中，n的值从 data_series_val[0] 中获取
                        lastest_data_key_in_redis = "StatusData_%s_%s_latest" % (self.client_id, self.service_name)
                        data_set = self.get_data_slice(lastest_data_key_in_redis, data_series_val[0])
                        if data_set.__len__() > 0:
                            # 接下来拿这个data_set交给下面这个方法,让它算出优化的结果来
                            optimized_data = self.get_optimized_data(data_series_key_in_redis, data_set)
                            if optimized_data:
                                self.save_optimized_data(data_series_key_in_redis, optimized_data)
                # 同时确保数据在redis中的存储数量不超过settings中指定 的值
                if self.redis_conn.llen(data_series_key_in_redis) >= data_series_val[1]:
                    # self.redis_conn.ltrim(data_series_key_in_redis,0,data_series_val[1])
                    self.redis_conn.lpop(data_series_key_in_redis)  # 删除最旧的一个数据
        else:
            print("report data is invalid::", self.data)
            raise ValueError

    def save_optimized_data(self, data_series_key_in_redis, optimized_data):
        self.redis_conn.rpush(data_series_key_in_redis, json.dumps([optimized_data, time.time()]))

    def get_data_slice(self, lastest_data_key, optimization_interval):
        """
        取出 当前时间截止到 optimization_interval 前的数据
        :param lastest_data_key:
        :param optimization_interval: 要取出数据相对于当前时间的时间间隔，单位：秒
        :return: 数据表中最近 optimization_interval 秒的数据
        """
        all_real_data = self.redis_conn.lrange(lastest_data_key, 1, -1)
        data_set = []
        for item in all_real_data:
            data = json.loads(item)
            if len(data) == 2:
                service_data, last_save_time = data
                if time.time() - last_save_time <= optimization_interval:
                    data_set.append(data)
                else:
                    pass

        return data_set

    def get_optimized_data(self, data_set_key, raw_service_data):
        """
        计算出 data_set中的 max、min、min(排好序之后的中间值),ava(average，平均值)
        :param data_set_key: 优化的数据需要保存的数据库表
        :param raw_service_data: 需要优化的数据
        :return:
        """
        service_data_keys = raw_service_data[0][0].keys()  # [iowait, idle,system...]
        first_service_data_point = raw_service_data[0][0]
        # 创建一个空的字典，保存优化后的数据
        optimized_dic = {}
        # 有些数据是直接按指标存储的，比如CPU，可以直接迭代；但是有一些是存放在 data中的，比如网卡，因为网卡有 etho、lo...等
        # 不同的网卡类型，etho中lo中都有相同的 key，迭代的时候，需要先取出data中数据再迭代
        if 'data' not in service_data_keys:
            for key in service_data_keys:
                # 先按指标把数据分别存储
                optimized_dic[key] = []
            # 为了临时存最近n分钟的数据 ,把它们按照每个指标都搞成一个一个列表,来存最近N分钟的数据
            tmp_data_dic = copy.deepcopy(optimized_dic)
            for service_data_item, last_save_time in raw_service_data:  # loop 最近n分钟的数据
                for service_index, v in service_data_item.items():
                    try:
                        tmp_data_dic[service_index].append(round(float(v), 2))
                    except ValueError:
                        pass
            for service_k, v_list in tmp_data_dic.items():
                avg_res = self.get_average(v_list)
                max_res = self.get_max(v_list)
                min_res = self.get_min(v_list)
                mid_res = self.get_mid(v_list)
                optimized_dic[service_k] = [avg_res, max_res, min_res, mid_res]
        else:
            for service_item_key, v_dic in first_service_data_point['data'].items():
                # service_item_key 相当于lo,eth0,... , v_dic ={ t_in:333,t_out:3353}
                optimized_dic[service_item_key] = {}
                for k2, v2 in v_dic.items():
                    optimized_dic[service_item_key][k2] = []  # {etho0:{t_in:[],t_out:[]}}

            tmp_data_dic = copy.deepcopy(optimized_dic)
            if tmp_data_dic:  # 由于客户端数据报错，有可能这里的数据是空的
                print('tmp data dic:', tmp_data_dic)
                for service_data_item, last_save_time in raw_service_data:  # loop最近n分钟数据
                    for service_index, val_dic in service_data_item['data'].items():
                        # print(service_index,val_dic)
                        # service_index这个值 相当于eth0,eth1...
                        for service_item_sub_key, val in val_dic.items():
                            # 上面这个service_item_sub_key相当于t_in,t_out
                            # if service_index == 'lo':
                            # print(service_index,service_item_sub_key,val)
                            tmp_data_dic[service_index][service_item_sub_key].append(round(float(val), 2))
                            # 上面的service_index变量相当于 eth0...
                for service_k, v_dic in tmp_data_dic.items():
                    for service_sub_k, v_list in v_dic.items():
                        avg_res = self.get_average(v_list)
                        max_res = self.get_max(v_list)
                        min_res = self.get_min(v_list)
                        mid_res = self.get_mid(v_list)
                        optimized_dic[service_k][service_sub_k] = [avg_res, max_res, min_res, mid_res]
            else:
                print("\033[41;1mMust be sth wrong with client report data\033[0m")
        print("optimized empty dic:", optimized_dic)

        return optimized_dic

    def get_average(self, data_set):
        if data_set.__len__ > 0:
            return sum(data_set) / len(data_set)
        else:
            return 0

    def get_max(self, data_set):
        if data_set.__len__ > 0:
            return max(data_set)
        else:
            return 0

    def get_min(self, data_set):
        if data_set.__len__ > 0:
            return min(data_set)
        else:
            return 0

    def get_mid(self, data_set):
        data_set.sort()
        # [1,4,99,32,8,9,4,5,9]
        # [1,3,5,7,9,22,54,77]
        if data_set.__len__ > 0:
            return data_set[len(data_set) / 2]
        else:
            return 0
