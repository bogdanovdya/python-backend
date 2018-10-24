def start_consume_mail():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='queue_mail', durable=True)
        channel.basic_consume(callback_mail,
                              queue='queue_mail',
                              no_ack=True)

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue mail: %s" % str(exc))

    connection.close()
    sys.exit(1)

def start_consume_sms():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='queue_sms', durable=True)
        channel.basic_consume(callback_sms,
                              queue='queue_sms',
                              no_ack=True
                              )

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue sms: %s" % str(exc))
    connection.close()
    sys.exit(1)

def start_consume_telegram():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='queue_tlgrm', durable=True)
        channel.basic_consume(callback_telegram,
                              queue='queue_tlgrm',
                              no_ack=True
                              )

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue tlgrm: %s" % str(exc))

    connection.close()
    sys.exit(1)