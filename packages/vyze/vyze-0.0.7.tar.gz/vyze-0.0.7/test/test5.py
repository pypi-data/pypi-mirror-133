from src import vyze

if __name__ == "__main__":
    client = vyze.Client()
    client.login('jom', 'testtest')
    # client.use_universe('geo3')
    s = client.stream()
    s.start()
    s.subscribe(client.resolve('base.object/base'), 'data', lambda msg: print('data', msg), payload=True)
    s.subscribe(client.resolve('base.object/base'), 'name', lambda msg: print('data', msg), payload=True)
    s.subscribe(client.resolve('base.object/base'), 'add_target', lambda msg: print('data', msg), payload=True)
    s.subscribe(client.resolve('base.object/base'), 'add_special', lambda msg: print('data', msg), payload=True)
    s.subscribe(client.resolve('base.object/base'), 'delete_object', lambda msg: print('data', msg), payload=True)
    s.join()
