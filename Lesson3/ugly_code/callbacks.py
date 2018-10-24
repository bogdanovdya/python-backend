def callback_one(ch, method, properties, body):
    row = create_one(body)
    db_result = db_process_one(row)
    result = event_update_one(db_result)
    if result:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)


def callback_two(ch, method, properties, body):
    row = create_two(body)
    db_result = db_process_two(row)
    result = event_update_two(db_result)
    if result:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)


def callback_three(ch, method, properties, body):
    row = create_three(body)
    db_result = db_process_three(row)
    if db_result:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        ch.basic_nack(delivery_tag=method.delivery_tag)

