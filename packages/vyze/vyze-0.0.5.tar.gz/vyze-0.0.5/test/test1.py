from src import vyze

if __name__ == "__main__":
    client = vyze.Client()
    client.login('Julian', 'goalfoev8')
    client.use_universe('geo3')
    obj = client.create_object(['base.object'], 'b2b981b1a7659088d3bcfe27b9e514fe', 'test_object')
    # print(obj)
    # client.delete_object(obj['id'])
    # obj = client.get_object(obj['id'])
    # print(obj)
    s = client.stream()
    # t = threading.Thread(target=s.run)
    # t.start()

    s.start()

    s.subscribe(obj['id'], 'data', lambda msg: print('data', msg))
    s.subscribe(obj['id'], 'name', lambda msg: print('name', msg), payload=True)

    client.set_data(obj['id'], bytes('test123', 'UTF8'))
    client.set_name(obj['id'], 'hello_obj')

    obj = client.get_object(obj['id'])
    data = client.get_data(obj['id'])

    print(obj)
    print(data)

    s.join()

    # t.join()
