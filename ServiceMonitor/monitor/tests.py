"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import json

# from django.test import TestCase
#
#
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)


def data_process():
    data = """
        {"127.0.0.1":{"Service": {"Ufa": {"unode": "started", "CENTER_NODE_ADDR": "http://127.0.0.1:9090/uctr/stor",
        "uctr": "started"}, "Xserver": {"xserver.mysql.host": "jdbc:mysql://127.0.0.1", "server": "started"}, "Mysql":
         {"server": "started"}}, "Server": {"MEM": {"swap_used": "0B", "swap_free": "2.0G", "mem_buffers": "106.7M",
         "mem_used": "1.2G", "mem_total": "1.8G", "mem_used_rate": "65.17", "mem_free_rate": "34.83", "mem_cached":
         "505.7M", "swap_total": "2.0G", "mem_free": "652.6M", "swap_used_rate": "0.00", "swap_free_rate": "100.00"},
          "DISK": [{"used": "6.4G", "free": "10.9G", "fstype": "ext4", "dev": "/dev/mapper/VolGroup-lv_root",
          "path": "/", "total": "17.3G", "used_rate": "37.11"}, {"used": "38.7M", "free": "445.5M", "fstype": "ext4",
          "dev": "/dev/sda1", "path": "/boot", "total": "484.2M", "used_rate": "8.00"}], "CPU": {"cores": [{"model":
          "Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz", "bits": "64bit"}], "cpu_count": 1, "core_count": 1}}}}
    """
    upload_data = {}
    service_data = {}
    server_data = {}
    data = json.loads(data)
    for ip in data:
        service_data = data[ip]['Service']
        server_data = data[ip]['Server']
        print(service_data)

    for service_name in service_data:
        upload_data[service_name] = {}
        for service_index in service_data[service_name]:
            upload_data[service_name][service_index] = service_data[service_name][service_index]
    #         print('=======================================================')
    #         print(type(service_name))
    #         print(type(service_index))
    #         print('=======================================================')
    print('=======================================================')
    print(json.dumps(upload_data))

if __name__ == "__main__":
    data_process()

