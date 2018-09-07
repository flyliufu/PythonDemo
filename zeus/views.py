# -*- coding: utf-8 -*-

import logging
import hashlib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .controller.BusinessController import BusinessController
from django.core.cache import caches

logger = logging.getLogger("django.request")


# django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def token(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = 'weixin'
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hash_str = ''.join([s for s in hashlist])
        hash_str = hashlib.sha1(hash_str.encode()).hexdigest()
        if hash_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("field")
    else:
        body = request.body
        logger.debug(
            '''
            =========REQUEST=========
            %s
            =========================
            ''' % body.decode("utf-8")
        )
        other_content = BusinessController().auto_reply(body)
        logger.debug(
            '''
            =========RESPONSE========
            %s
            =========================
            ''' % other_content
        )
        return HttpResponse(other_content)


var = caches['default']
var.set("aaa", 'bbb', timeout=5)


def index(request):
    context = {
        "name": var.get('aaa')
    }
    return render(request, 'zeus/index.html', context=context)
