def callback_sms(ch, method, properties, body):
    send_sms(body)


def callback_telegram(ch, method, properties, body):
    send_telegram(body)


def callback_mail(ch, method, properties, body):
    send_mail(body)


def callback_telegram(ch, method, properties, body):
    send_telegram(body)


def callback_mail(ch, method, properties, body):
    send_mail(body)