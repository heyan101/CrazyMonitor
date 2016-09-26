# coding:utf8

import json

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from backends.doc_process import DocUtils

# redis connection
# REDIS_CONN = redis_conn.redis_conn(settings)


@csrf_exempt
def service_data_report(request):
    if request.method == 'POST':
        data = request.POST
        docUtils = DocUtils()
        docUtils.parseDataProduceDoc(data)

    return HttpResponse(json.dumps('{"status":"OK"}'))
