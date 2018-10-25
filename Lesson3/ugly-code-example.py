#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import os
import sys
import json
import syslog
import time
import re
import requests
import telegram
from threading import Thread


def supervisor(thr_list):
    thr = []

    for thread_name in thr_list:
        thr.append(None)

    while True:
        i = 0
        for thread_name in thr_list:
            if not thr[i] or not thr[i].is_alive():
                thr[i] = Thread(target=thread_name)
                thr[i].daemon = True
                thr[i].start()
                syslog.syslog("Starting thread for: %s" % str(thread_name))
            thr[i].join(1)
            i = i + 1

        time.sleep(10)


class ICreate:
    def __init__(self, body_msg):
        _tt = json.loads(body_msg)
        try:
            syslog.syslog('Message: {} {} {}'.format(_tt['hostname'].encode('utf-8'),
                                                     _tt['message'].encode('utf-8'),
                                                     _tt['state-trigger'].encode('utf-8')))
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))

    def create_msg(self, tt):
        """"creating message"""


class CreateOne(ICreate):
    def create_msg(self, tt):
        try:
            row = [
                tt['hostname'].encode('utf-8'),
                tt['hostname'].encode('utf-8'),
                tt['state-trigger'].encode('utf-8'),
                "Автоматически создано \nevent: " +
                str(tt['event'].encode('utf-8')),
                tt['check-type'].encode('utf-8'),
                int(tt['trigger']),
                tt['message'].encode('utf-8'),
                tt.get('zhost', 'some.host').encode('utf-8')
            ]
            return row

        except Exception as exc:
            syslog.syslog("Error while creating: %s" % exc)
            return False


class CreateTwo(ICreate):
    def create_msg(self, tt):
        try:
            row = [
                tt['hostname'].encode('utf-8'),
                tt['ip-address'].encode('utf-8'),
                tt['state-trigger'].encode('utf-8'),
                tt['message'].encode('utf-8'),
                tt['comment'].encode('utf-8'),
                tt['trigger'].encode('utf-8'),
                "Автоматически создано " +
                tt['prefix'].encode('utf-8')+"\nevent: " +
                tt['event'].encode('utf-8'),
                tt.get('zhost', 'some.host').encode('utf-8')
            ]
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % exc)
            return False


class CreateThree(ICreate):
    def create_msg(self, tt):
        try:
            row = [tt['hostname'].encode(
                'utf-8'), tt['state-trigger'].encode('utf-8'), tt['trigger'].encode('utf-8')]
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % (exc))
            return False


class CreateSms(ICreate):
    def create_msg(self, tt):
        number = tt['number']
        subject = tt['subject']
        message = tt['message']

        message = subject + " " + message
        message = message.replace('\n', '')
        message = message[:70].encode('utf-8')

        row = {
            "message": message,
            "number": number,
        }
        return row


class CreateMail(ICreate):
    def create_msg(self, tt):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.header import Header
        from validate_email import validate_email

        try:
            my_mail = 'mail@mail.server'
            mail_is_valid = validate_email(tt['mail'])

            if mail_is_valid is not True:
                raise Exception("invalid e-mail: " + tt['mail'])

            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(tt['subject'], 'utf-8')
            msg['From'] = my_mail
            msg['To'] = tt['mail']

            msgText = MIMEText(tt['message'].encode(
                'utf-8'), 'plain', 'utf-8')
            msg.attach(msgText)

            s = smtplib.SMTP('mail.server')
            s.sendmail(my_mail, tt['mail'], msg.as_string())

            syslog.syslog("Sending email-massage to: %s" % (tt['mail']))
        except Exception as exc:
            syslog.syslog("Error while sending e-mail: %s" % (exc))

        finally:
            if s:
                s.quit()


class CreateTelegram(ICreate):
    def create_msg(self, tt):
        row = tt
        return row


class CreateMediator:
    def __init__(self, queue, body_msg):
        _queue = queue
        create_dict = {
            'queue_one': CreateOne(body_msg),
            'queue_two': CreateTwo(body_msg),
            'queue_three': CreateThree(body_msg),
            'queue_sms': CreateSms(body_msg),
            'queue_mail': CreateMail(body_msg),
            'queue_Tgm_1': CreateTelegram(body_msg),
            'queue_tlgrm': CreateTelegram(body_msg)
        }
        try:
            create_dict[_queue]
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))


class TelegramApi:
    def __init__(self, token, proxy={}):
        self.BOT_TOKEN = token
        self.cmd = {"stat": "getMe", "send": "sendMessage"}
        if proxy:
            ip = proxy['ip']
            port = proxy['port']
            user = proxy['user']
            passwd = proxy['password']
            pp = telegram.utils.request.Request(proxy_url='socks5://%s:%s' % (
                ip, port), urllib3_proxy_kwargs={'username': user, 'password': passwd})
        else:
            pp = telegram.utils.request.Request()
        self.bot = telegram.Bot(token=self.BOT_TOKEN, request=pp)

    def stat(self):
        # cmd=self.cmd["stat"]
        try:
            pass
        except Exception as err:
            messToSyslog = "Fail to read telegram_bot status: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)

    def send(self, chat, mess):
        # cmd = self.cmd["send"]
        mess = mess.encode('utf-8')
        try:
            self.bot.sendMessage(chat, mess)
            return True
        except Exception as err:
            messToSyslog = "Fail to sendmessage via telegram_bot: %s" % (err)
            syslog.syslog('-----------------------------------------')
            syslog.syslog(" %s" % messToSyslog)


class IHandlerFactory:

    queue = None
    params = None

    def callback(self, ch, method, properties, body):
        """"creating callback"""

    def start_consume(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_consume(self.callback,
                                  queue=self.queue,
                                  no_ack=False, exclusive=False)
            channel.basic_qos(prefetch_count=1)
            channel.start_consuming()
        except Exception as exc:
            # channel.stop_consuming()
            syslog.syslog("Error while consuming %s queue: %s" %
                          (self.queue, str(exc)))
        connection.close()
        sys.exit(1)

        connection.close()


class HandlerNumberFactory(IHandlerFactory):

    params = {"procedure": "procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);"}

    def callback(self, ch, method, properties, body):
        row = CreateMediator(self.queue, body)
        db_result = CorporateDB(self.params["procedure"])
        if db_result:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)


class HandlerOne(HandlerNumberFactory):
    def __init__(self):
        self.queue = "queue_one"


class HandlerTwo(HandlerNumberFactory):
    def __init__(self):
        self.queue = "queue_two"


class HandlerThree(HandlerNumberFactory):
    def __init__(self):
        self.queue = "queue_three"
        self.params = {"procedure": "procedure_two(:1, :2, :3);"}


class HandlerMessageFactory(IHandlerFactory):
    def callback(self, ch, method, properties, body):
        CreateMediator(self.queue, body)


class HandlerTelegram(HandlerMessageFactory):
    def __init__(self):
        self.queue = "queue_tlgrm"
        self.params = {"telegram": {"token": "id:token",
                                    "base_url": "https://api.telegram.org/bot",
                                    'proxy': {
                                        'ip': '0.0.0.0',
                                        'port': 9999, 'user': 'some_user', 'password': 'some_password'}}}


class HandlerPsevdoTelegram(HandlerMessageFactory):
    def __init__(self):
        self.queue = "queue_tlgrm"
        self.params = {'url_in': 'some url in'}


class HandlerMail(HandlerMessageFactory):
    def __init__(self):
        self.queue = "mail"
        self.params = "mail"


class HandlerSms(IHandlerFactory):
    def __init__(self):
        self.queue = "sms"
        self.params = {"mail": {}}

    def callback(self, ch, method, properties, body):
        row = CreateMediator(self.queue, body)
        try:
            db_result = CorporateDB(self.params[self.queue]["procedure" % (row['message'])])
            if db_result:
                syslog.syslog("Sending SMS message to: %s" % (row['number']))
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            syslog.syslog("Error while sending SMS notification: %s" % (exc))


class CorporateDB:
    _instance = None

    def __new__(cls, url_in):
        cls.connection = dbModule.Connection("login/password")
        if cls._instance is None:
            cls._instance = super(CorporateDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, url_in):
        self.cursor = self.connection.cursor()
        self.cursor.execute('''BEGIN
                            %s;
                            END;''' % url_in)


if __name__ == "__main__":
    syslog.openlog('some_tag', syslog.LOG_PID, syslog.LOG_NOTICE)

    try:
        thr_list = [
            HandlerOne,
            HandlerTwo,
            HandlerThree,
            HandlerSms,
            HandlerMail,
            HandlerTelegram,
            HandlerPsevdoTelegram
        ]
        supervisor(thr_list)

    except KeyboardInterrupt:
        print("EXIT")
        raise
