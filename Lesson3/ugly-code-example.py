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


class Create:
    def __init__(self, queue, body_msg):
        _queue = queue
        _tt = json.loads(body_msg)
        create_dict = {
            'queue_one': self.create_one(_tt),
            'queue_two': self.create_two(_tt),
            'queue_three': self.create_three(_tt),
            'queue_sms': self.create_sms(_tt),
            'queue_mail': self.create_mail(_tt),
            'queue_Tgm_1': self.telegram,
            'queue_tlgrm': self.telegram,
        }
        try:
            create_dict[_queue]
            syslog.syslog('Message: {} {} {}'.format(_tt['hostname'].encode('utf-8'),
                                                     _tt['message'].encode('utf-8'),
                                                     _tt['state-trigger'].encode('utf-8')))
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))

    def create_one(self, tt):
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

    def create_two(self, tt):
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

    def create_three(self, tt):
        try:
            row = [tt['hostname'].encode(
                'utf-8'), tt['state-trigger'].encode('utf-8'), tt['trigger'].encode('utf-8')]
            return row
        except Exception as exc:
            syslog.syslog("Error while creating: %s" % (exc))
            return False

    def create_sms(self, smsDict):

        number = smsDict['number']
        subject = smsDict['subject']
        message = smsDict['message']

        message = subject+" "+message
        message = message.replace('\n', '')
        message = message[:70].encode('utf-8')

        row = {
            "message": message,
            "number": number,
        }
        return row

    def create_mail(self, mailDict):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.header import Header
        from validate_email import validate_email

        try:
            my_mail = 'mail@mail.server'
            mail_is_valid = validate_email(mailDict['mail'])

            if mail_is_valid is not True:
                raise Exception("invalid e-mail: " + mailDict['mail'])

            msg = MIMEMultipart('alternative')
            msg['Subject'] = Header(mailDict['subject'], 'utf-8')
            msg['From'] = my_mail
            msg['To'] = mailDict['mail']

            msgText = MIMEText(mailDict['message'].encode(
                'utf-8'), 'plain', 'utf-8')
            msg.attach(msgText)

            s = smtplib.SMTP('mail.server')
            s.sendmail(my_mail, mailDict['mail'], msg.as_string())

            syslog.syslog("Sending email-massage to: %s" % (mailDict['mail']))
        except Exception as exc:
            syslog.syslog("Error while sending e-mail: %s" % (exc))

        finally:
            if s:
                s.quit()

    def telegram(self, body_msg):
        row = body_msg
        return


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


class Handler:
    def __init__(self, queue):
        self.queue = queue

        self.params = {"telegram": {"token": "id:token",
                                    "base_url": "https://api.telegram.org/bot",
                                    'proxy': {
                                        'ip': '0.0.0.0',
                                        'port': 9999, 'user': 'some_user', 'password': 'some_password'}},
                       "to_db": {'url_in': 'some url in'},
                       "mail": {},
                       "sms": {"procedure": "send_procedure(%s);"},
                       "queue_one": {"procedure": "procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);"},
                       "queue_two": {"procedure": "procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);"},
                       "queue_three": {"procedure": "procedure_two(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);"}}

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

    def callback(self, ch, method, properties, body):
        if ch in ["queue_one", "queue_one", "queue_one"]:
            row = Create(ch, body)
            db_result = CorporateDB(self.params[ch]["procedure"])
            if db_result:
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag)

        if ch == "sms":
            row = Create(ch, body)
            try:
                db_result = CorporateDB(self.params[ch]["procedure" % (row['message'])])
                if db_result:
                    syslog.syslog("Sending SMS message to: %s" % (row['number']))
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                else:
                    ch.basic_nack(delivery_tag=method.delivery_tag)
            except Exception as exc:
                syslog.syslog("Error while sending SMS notification: %s" % (exc))

        if ch in ["queue_Tgm_1", "queue_tlgrm", "mail"]:
            Create(ch, body)


#corporateDB class
class CorporateDB:
    def __init__(self, url_in):
        self.connection = dbModule.Connection("login/password")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''BEGIN
                            %s;
                            END;''' % url_in)

    def telegram_procedure_exec(self, group, message):
        self.cursor.execute("""BEGIN
                        %s;
                        COMMIT;
                        END;""" % message, group=int(group), result_out=result_out, message_out=message_out)
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        return result_out.getvalue(), message_out.getvalue()


if __name__ == "__main__":
    syslog.openlog('some_tag', syslog.LOG_PID, syslog.LOG_NOTICE)

    try:
        thr_list = []
        for n in ["queue_Tgm_1", "queue_tlgrm", "queue_one", "queue_two", "queue_three", "queue_mail", "queue_sms"]:
            thread = Handler(n)
            thr_list.append(thread.start_consume)

        supervisor(thr_list)

    except KeyboardInterrupt:
        print("EXIT")
        raise
