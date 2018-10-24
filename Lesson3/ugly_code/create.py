def create_one(body_msg):
    tt = json.loads(body_msg)

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

        syslog.syslog('Message: {} {} {}'.format(tt['hostname'].encode(
            'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
        return row
    except Exception as exc:
        syslog.syslog("Error while creating: %s" % exc)
        return False

def create_two(body_msg):
    tt = json.loads(body_msg)
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

        syslog.syslog('Message: {} {} {}'.format(tt['hostname'].encode(
            'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
        return row
    except Exception as exc:
        syslog.syslog("Error while creating: %s" % exc)
        return False

def create_three(body_msg):
    tt = json.loads(body_msg)
    try:
        row = [tt['hostname'].encode(
            'utf-8'), tt['state-trigger'].encode('utf-8'), tt['trigger'].encode('utf-8')]

        syslog.syslog('Three message: {} {} {}'.format(tt['hostname'].encode(
            'utf-8'), tt['message'].encode('utf-8'), tt['state-trigger'].encode('utf-8')))
        return row
    except Exception as exc:
        syslog.syslog("Error while creating: %s" % (exc))
        return False
