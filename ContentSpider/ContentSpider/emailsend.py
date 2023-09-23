#-*- coding: utf-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-12-04
:python version: 3.6

---------------
'''
import smtplib
from email.mime.text import MIMEText

import logging


class EmailSend(object):
    def __init__(self):
        self.logging = logging.getLogger('Waring')
        self.email_host = 'smtp.qq.com'
        self.email_port = '465'
        self.email_pass = '*********' # 自己的授权码

    def send_text_email(self, from_addr, to_addrs, subject, content):
        self.logging.warning('send_text_email is willed 丢弃')
        self.logging.error('send_text_email is None')
        message_text = MIMEText(content, 'plain', 'utf8')
        message_text['From'] = from_addr
        message_text['To'] = to_addrs
        message_text['Subject'] = subject

        try:
            # 在创建客户端对象的同时，连接到邮箱服务器。
            client = smtplib.SMTP_SSL(host=self.email_host, port=self.email_port)
            login_result = client.login(from_addr, self.email_pass)
            if login_result and login_result[0] == 235:
                print('登录成功')
                client.sendmail(from_addr, to_addrs, message_text.as_string())
                print('邮件发送成功')
            else:
                print('邮件发送异常：', login_result[0], login_result[1])
        except Exception as e:
            # print('连接邮箱服务器异常：',e)
            self.logging.error('连接邮箱服务器异常：{}'.format(e))

    def send_image_email(self):
        pass

    def send_word_email(self):
        pass

    def send_video_email(self):
        pass
