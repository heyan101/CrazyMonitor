# coding:utf8

"""
后台数据优化
"""

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
