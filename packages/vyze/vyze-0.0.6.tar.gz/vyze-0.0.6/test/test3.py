import datetime
import random
import threading
from time import sleep

from src import vyze

if __name__ == "__main__":
    t1 = datetime.datetime.now()

    client = vyze.Client(system_url='http://localhost:9131/access/', stream_url='wss://localhost:9131/stream/', app_url='http://localhost:9150/')
    client.login('jom', 'goalfoev8')
    client.use_universe('test')

    t2 = datetime.datetime.now()

    user_ids = client.get_specials('user')

    t3 = datetime.datetime.now()

    uname = 'Kundai6'

    usr = None
    for user_id in user_ids:
        name = client.get_value(user_id, 'user#name')
        if name == uname:
            usr = user_id
            break

    print(usr)

    t4 = datetime.datetime.now()

    if not usr:
        u = client.create_object(['user'])
        client.set_value(u['id'], 'user#name', uname)
        usr = u['id']

        activities = 'AABCAAAAAAADAAAABAAACAA'
        time = datetime.datetime(2022, 1, 4)

        for a in activities:
            client.add_value(usr, 'user#activity', a, time=time)
            time += datetime.timedelta(minutes=5)

    t5 = datetime.datetime.now()

    print(client.get_values(usr, 'user#activity'))

    t6 = datetime.datetime.now()

    print(t2 - t1)
    print(t3 - t2)
    print(t4 - t3)
    print(t5 - t4)
    print(t6 - t5)
