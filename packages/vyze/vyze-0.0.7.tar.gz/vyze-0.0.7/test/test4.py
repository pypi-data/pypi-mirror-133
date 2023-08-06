import datetime
import json

from src import vyze
from src.vyze import EVENT_DATA

if __name__ == "__main__":
    client = vyze.Client(system_url='http://localhost:9131/access/', stream_url='ws://localhost:9131/stream', app_url='http://localhost:9150/')
    client.login('vingi', 'testtest')
    client.use_universe('test2')

    persons = client.get_specials('person')
    for person in persons:
        name = client.get_value(person, 'person#name')

        # n = datetime.datetime.now()
        # for i in range(10):
        #     print(client.add_value(person, 'person#heartrate', 80, time=n + datetime.timedelta(minutes=i * 5)))

        print(client.get_dict_values(person, {'name1': 'person#name', 'name2': 'person#name'}, ['name1', 'name2']))
