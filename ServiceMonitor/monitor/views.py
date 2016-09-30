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
        print('===========================================')
        data = request.POST['data']
        # encode
        data = urllib.unquote(data)
        print(data)

        # data decrypt
        openssl = Openssl()
        status, result = openssl.decryptData(data)
        if status != 0:  # error
            stat = 'ERROR_OPENSSL_ENCRYPT'
        else:
            doc = DocUtils()
            doc.parseDataProduceDoc(result)

    return HttpResponse(json.dumps('{"stat":"%s"}' % stat))
