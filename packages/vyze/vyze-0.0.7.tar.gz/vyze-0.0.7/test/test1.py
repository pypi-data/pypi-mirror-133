from src import vyze

if __name__ == "__main__":
    # client = vyze.Client(system_url='http://localhost:9131/access/', stream_url='ws://localhost:9131/stream', app_url='http://localhost:9150/')
    client = vyze.Client()
    client.login('jom', 'testtest')
    client.use_universe('geo3')
    obj = client.create_object(['base.object'])
    # print(obj)
    # client.delete_object(obj['id'])
    # obj = client.get_object(obj['id'])
    # print(obj)
    s = client.stream()
    # t = threading.Thread(target=s.run)
    # t.start()

    s.start()

    s.subscribe(obj['id'], 'data', lambda msg: print('data', msg), payload=True)
    s.subscribe(obj['id'], 'name', lambda msg: print('name', msg), payload=True)

    client.set_data(obj['id'], bytes('test123', 'UTF8'))
    client.set_name(obj['id'], 'hello_obj')

    obj = client.get_object(obj['id'])
    data = client.get_data(obj['id'])

    print(obj)
    print(data)

    s.join()

    # t.join()
