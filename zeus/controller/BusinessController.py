from zeus.util.MsgUtil import MsgUtil

# 微信服务器推送消息是xml的，根据利用ElementTree来解析出的不同xml内容返回不同的回复信息，就实现了基本的自动回复功能了，也可以按照需求用其他的XML解析方法
import xml.etree.ElementTree as et
import logging

logger = logging.getLogger("django.request")


class BusinessController:

    def auto_reply(self, body):
        xml_data = et.fromstring(body)
        msg_type = xml_data.find('MsgType').text
        ToUserName = xml_data.find('ToUserName').text
        FromUserName = xml_data.find('FromUserName').text
        CreateTime = xml_data.find('CreateTime').text
        # MsgId = xml_data.find('MsgId').text

        reply_msg = MsgUtil(FromUserName, ToUserName)
        content = "您好,欢迎来到Python学习!"
        if msg_type == 'event':  # 触发事件消息类型
            event = xml_data.find('Event').text
            eventKey = xml_data.find('EventKey').text
            if event == 'subscribe':  # 订阅事件
                return reply_msg.send_text("终于等到你了！欢迎关注我们，未来我们一起成长！！！")
            if event == 'unsubscribe':  # 取消订阅事件
                pass

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

        return reply_msg.send_text(content)
