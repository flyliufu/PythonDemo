# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import logging

import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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
        othercontent = autoreply(request)
        return HttpResponse(othercontent)


# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as ET


def autoreply(request):
    try:
        webData = request.body
        logger.debug(
            '''
            =========REQUEST=========
            %s
            =========================
            ''' % webData.decode("utf-8")
        )
        xml_data = ET.fromstring(webData)

        msg_type = xml_data.find('MsgType').text
        ToUserName = xml_data.find('ToUserName').text
        FromUserName = xml_data.find('FromUserName').text
        CreateTime = xml_data.find('CreateTime').text
        MsgType = xml_data.find('MsgType').text
        MsgId = xml_data.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = "您好,欢迎来到Python大学习!希望我们可以一起进步!"
            reply_msg = TextMsg(toUser, fromUser, content)
            print("成功了!!!!!!!!!!!!!!!!!!!")
            print(reply_msg)
            return reply_msg.send()

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()
        elif msg_type == 'link':
            content = "链接已收到,谢谢"
            reply_msg = TextMsg(toUser, fromUser, content)
            return reply_msg.send()

    except Exception as Argument:
        return Argument


class Msg(object):
    def __init__(self, xml_data):
        logger.debug(xml_data)
        self.ToUserName = xml_data.find('ToUserName').text
        self.FromUserName = xml_data.find('FromUserName').text
        self.CreateTime = xml_data.find('CreateTime').text
        self.MsgType = xml_data.find('MsgType').text
        self.MsgId = xml_data.find('MsgId').text


import time


class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        __xml = XmlForm.format(**self.__dict)
        logger.debug(
            '''
            =========RESPONSE========
            %s
            =========================
            ''' % __xml
        )
        return __xml
