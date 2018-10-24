def start_consume_one():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='queue_one', durable=True)
        channel.basic_consume(callback_one,
                              queue='queue_one',
                              no_ack=False, arguments={"x-priority": 5})

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue one: %s" % exc)

    connection.close()
    sys.exit(1)

def start_consume_two():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='queue_two', durable=True)
        channel.basic_consume(callback_two,
                              queue='queue_two',
                              no_ack=False)

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue two: %s" % str(exc))

    connection.close()
    sys.exit(1)

def start_consume_three():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='queue_three', durable=True)
        channel.basic_consume(callback_three,
                              queue='queue_three',
                              no_ack=False)

        channel.basic_qos(prefetch_count=1)
        channel.start_consuming()
    except Exception as exc:
        channel.stop_consuming()
        syslog.syslog("Error while consuming queue three: %s" % str(exc))

    connection.close()
    sys.exit(1)