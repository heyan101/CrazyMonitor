# coding:utf8

import threading
import time
import urllib
import urllib2

from conf import settings
import json


class ClientHandle(object):

    def __init__(self):
        # 用来存放需要监控的服务信息
        self.monitored_services = {}

    def forever_run(self):
        """
        start the client program forever
        :return:
        """
        exit_flag = False
        # 配置文件更新时间，每隔一定时间就会去服务端获取一次最新的配置
        config_last_update_time = 0

        while not exit_flag:
            if time.time() - config_last_update_time > settings.configs['ConfigUpdateInterval']:
                # 加载配置文件
                self.load_last_configs()
                print("Loaded latest config:", self.monitored_services)
                # 更新下次获取配置文件的时间
                config_last_update_time = time.time()

            # start to monitor services
            for service_name, val in self.monitored_services['services'].items():
                # 这里是为了给每个服务添加一个时间，以便于判断启动的时间间隔
                if len(val) == 2:
                    self.monitored_services['services'][service_name].append(0)
                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:
                    print(last_invoke_time, time.time())
                    self.monitored_services['services'][service_name][2] = time.time()
                    # start a new thread to call each monitor plugin
                    t = threading.Thread(target=self.invoke_plugin, args=(service_name, val))
                    t.start()
                    print("Going to monitor [%s]" % service_name)
                else:
                    print("Going to monitor [%s] in [%s] secs" % (service_name,
                          monitor_interval - (time.time() - last_invoke_time)))
            time.sleep(1)

    def invoke_plugin(self, service_name, val):
        """
        invoke the monitor plugin here, and send the data to monitor server after plugin returned status data each time
        :param service_name:
        :param val: [pulgin_name,monitor_interval,last_run_time]
        :return:
        """
        # 通过反射加载插件
        plugin_name = val[0]
        if hasattr(plugin_api, plugin_name):
            func = getattr(plugin_api, plugin_name)

    def load_last_configs(self):
        """
        Load the lotest monitor configs from monitor server
        :return:
        """
        request_type = settings.configs['urls']['get_configs'][1]
        url = '%s/%s' % (settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
        # 向服务端请求获取需要监控的数据
        latest_configs = self.url_request(request_type, url)
        latest_configs = json.loads(latest_configs)
        self.monitored_services.update(latest_configs)

    def url_request(self, action, url, **extra_data):
        '''
        cope with monitor server by url
        :param action: 'get' or 'post'
        :param url: witch url you want to request from the monitor server
        :param extra_data: extra parameters needed to be submited
        :return:
        '''
        abs_url = 'http://%s/%s/%s' % (settings.configs['Server'],
                                       settings.configs['ServerPort'],
                                       url)
        if action in ('get', 'GET'):
            print(abs_url, extra_data)
            try:
                req = urllib2.Request(abs_url)
                req_data = urllib2.open(req, timeout=settings.configs['RequestTimeout'])
                callback = req_data.read()
                return callback
            except urllib2.URLError, e:
                exit("\033[31;1m%s\033[0m" % e)
        elif action in ('post', 'POST'):
            try:
                data_encode = urllib.urlencode(extra_data['params'])
                req = urllib2.Request(url=abs_url, data=data_encode)
                res_data = urllib2.urlopen(req, timeout=settings.configs['RequestTimeout'])
                callback = res_data.read()
                callback = json.loads(callback)
                print "\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (action, abs_url, callback)
                return callback
            except Exception, e:
                exit("\033[31;1m%s\033[0m" % e)

