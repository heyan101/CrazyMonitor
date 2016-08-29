# coding:utf8

configs = {
    'HostID': 1,
    'Server': '127.0.0.1',
    'ServerPort': 8000,
    'urls': {
        'get_configs': ['api/client/config', 'get'],
        'server_report': ['api/client/service/report/', 'post'],
    },
    'RequestTimeout': 30,
    'ConfigUpdateInterval': 300,  #5 mins as default
}