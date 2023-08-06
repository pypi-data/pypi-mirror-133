import datetime
import random
import threading
from time import sleep

from src import vyze

if __name__ == "__main__":
    client = vyze.Client()
    client.login('jom', 'goalfoev8')
    client.use_universe('geo3')

    point_defs = {'time': 'path_point#time', 'longitude': 'point#longitude', 'latitude': 'point#latitude'}
    path_defs = {'color': 'path#color'}

    ids = []

    def create_obj():
        if random.random() < 0.5:
            obj = client.create_object(['path_point'], 'point1')
            client.set_dict_values(obj['id'], point_defs, {'time': datetime.datetime.now(), 'longitude': 12.54, 'latitude': -23.333})
            ids.append(obj['id'])
            print(obj['id'])
        else:
            obj = client.create_object(['path'], 'path1')
            client.set_dict_values(obj['id'], path_defs, {'color': 'red'})
            ids.append(obj['id'])
            print(obj['id'])

    start = datetime.datetime.now()

    threads = []
    parallel = 4
    for i in range(200):
        x = threading.Thread(target=create_obj)
        x.start()
        threads.append(x)
        while len(threads) > parallel:
            threads[0].join()
            threads = threads[1:]
    for x in threads:
        x.join()

    end = datetime.datetime.now()

    print(end - start)
