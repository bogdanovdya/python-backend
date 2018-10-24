def event_update(data):
    if not data:
        return False
    zhost, evid, NumTT = data

    server = 'server'
    if zhost == 'server2':
        server = 'server2'

    login = 'event_login'
    password = 'event_password'

    s = requests.Session()
    s.auth = (login, password)

    return True




def event_update_two(data):
    if not data:
        return False
    zhost, evid, NumTT = data

    server = 'server'
    if zhost == 'server2':
        server = 'server2'

    login = 'event_login'
    password = 'event_password'

    s = requests.Session()
    s.auth = (login, password)

    return True

def event_update_one(data):
    if not data:
        return False
    zhost, evid, NumTT = data

    server = 'server'
    if zhost == 'server2':
        server = 'server2'

    login = 'event_login'
    password = 'event_password'

    s = requests.Session()
    s.auth = (login, password)

    return True