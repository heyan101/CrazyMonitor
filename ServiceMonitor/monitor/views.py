# coding:utf8

import json
import urllib

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from monitor.backends.doc_process import DocUtils
from monitor.backends.openssl import Openssl


@csrf_exempt
def service_data_report(request):
    stat = 'OK'
    if request.method == 'POST':
        data = request.POST['data']
        # encode
        data = urllib.unquote(data)

        # data decrypt
        openssl = Openssl()
        status, result = openssl.decryptData(data)
        if status != 0:  # error
            stat = 'ERROR_OPENSSL_ENCRYPT'
        else:
            doc = DocUtils()
            result = """
                {"127.0.0.1":{"Service": {"Ufa": {"unode": "started", "CENTER_NODE_ADDR": "http://127.0.0.1:9090/uctr/stor",
                "uctr": "started"}, "Xserver": {"xserver.mysql.host": "jdbc:mysql://127.0.0.1", "server": "started"},
                "Mysql":{"server": "started"}}, "Server": {"MEM": {"swap_used": "0B", "swap_free": "2.0G",
                "mem_buffers": "106.7M","mem_used": "1.2G", "mem_total": "1.8G", "mem_used_rate": "65.17",
                "mem_free_rate": "34.83", "mem_cached":"505.7M", "swap_total": "2.0G", "mem_free": "652.6M",
                "swap_used_rate": "0.00", "swap_free_rate": "100.00"},"DISK": [{"used": "6.4G", "free": "10.9G",
                "fstype": "ext4", "dev": "/dev/mapper/VolGroup-lv_root", "path": "/","total": "17.3G", "used_rate": "37.11"},
                {"used": "38.7M", "free": "445.5M", "fstype": "ext4", "dev": "/dev/sda1","path": "/boot",
                "total": "484.2M", "used_rate": "8.00"}], "CPU": {"cores": [{"model": "Intel(R) Core(TM)i7-6700HQ CPU @ 2.60GHz",
                "bits": "64bit"}], "cpu_count": 1, "core_count": 1}}}}
                """
            doc.parseDataProduceDoc(result)

    return HttpResponse(json.dumps('{"stat":"%s"}' % stat))
