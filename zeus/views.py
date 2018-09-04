# -*- coding: utf-8 -*-

import logging

import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from zeus.util.MsgUtil import MsgUtil

# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as et

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
        other_content = auto_reply(body)
        logger.debug(
            '''
            =========RESPONSE========
            %s
            =========================
            ''' % other_content
        )
        return HttpResponse(other_content)


def auto_reply(body):
    xml_data = et.fromstring(body)
    msg_type = xml_data.find('MsgType').text
    ToUserName = xml_data.find('ToUserName').text
    FromUserName = xml_data.find('FromUserName').text
    CreateTime = xml_data.find('CreateTime').text
    MsgType = xml_data.find('MsgType').text
    MsgId = xml_data.find('MsgId').text

    content = "您好,欢迎来到Python学习!"
    if msg_type == 'text':
        content = "文本已收到,谢谢"
    elif msg_type == 'image':
        content = "图片已收到,谢谢"
    elif msg_type == 'voice':
        content = "语音已收到,谢谢"
    elif msg_type == 'video':
        content = "视频已收到,谢谢"
    elif msg_type == 'shortvideo':
        content = "小视频已收到,谢谢"
    elif msg_type == 'location':
        content = "位置已收到,谢谢"
    elif msg_type == 'link':
        content = "链接已收到,谢谢"

    reply_msg = MsgUtil(FromUserName, ToUserName, content)
    return reply_msg.send_text()
