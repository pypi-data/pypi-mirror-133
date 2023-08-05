import requests

from typing import Any

from .stream import Stream


class Client:

    def __init__(self, system_url='http://localhost:9131/access', stream_url='ws://localhost:9131/stream', app_url='http://localhost:9150'):
        self.__app_url = app_url
        self.__stream_url = stream_url
        self.__system_url = system_url

        self.__universe = ''

        self.__user_id = None
        self.__refresh_token = None
        self.__access_token = None
        self.__space_tokens = {}

        self.__cache = {}

    def login(self, username, password):
        resp = requests.post(f'{self.__app_url}/user/login', json={
            'username': username,
            'password': password,
        })

        if resp.status_code != 200:
            return False

        self.__user_id = resp.json()['userId']
        self.__refresh_token = resp.json()['refreshToken']

        self.__refresh()

        return True

    def use_universe(self, universe):
        self.__universe = universe

    def resolve(self, identifier):
        if isinstance(identifier, list):
            return [self.resolve(i) for i in identifier]

        identifier = f'{identifier}/{self.__universe}'

        obj = self.__cache.get(identifier)
        if obj is None:
            resp = requests.get(f'{self.__app_url}/universe/resolve', params={'i': identifier})
            obj = resp.json()
            self.__cache[identifier] = obj

        return obj

    def create_object(self, abstracts, space, name=''):
        return self.__post(f'{self.__system_url}/objects', {
            'abstracts': self.resolve(abstracts),
            'space': space,
            'name': name
        })['object']

    def get_object(self, id):
        return self.__get(f'{self.__system_url}/objects/{id}')['object']

    def delete_object(self, id):
        return self.__delete(f'{self.__system_url}/objects/{id}')

    def set_name(self, id, name: str):
        self.__post(f'{self.__system_url}/objects/{id}/name', {
            'name': name,
        })

    def get_data(self, id) -> bytes:
        return self.__get(f'{self.__system_url}/objects/{id}/data', is_json=False)

    def set_data(self, id, data: bytes):
        self.__post(f'{self.__system_url}/objects/{id}/data', data, is_json=False)

    def get_abstracts(self, id, include_self=False, include_direct=True, include_transitive=False):
        return self.__get(
            f'{self.__system_url}/objects/{id}/abstracts'
            f'?self={"1" if include_self else "0"}'
            f'&direct={"1" if include_direct else "0"}'
            f'&transitive={"1" if include_transitive else "0"}')['ids']

    def get_specials(self, id, include_self=False, include_direct=True, include_transitive=False):
        return self.__get(
            f'{self.__system_url}/objects/{id}/specials'
            f'?self={"1" if include_self else "0"}'
            f'&direct={"1" if include_direct else "0"}'
            f'&transitive={"1" if include_transitive else "0"}')['ids']

    def set_value(self, id, field, value):
        pass

    def add_value(self, id, field, value):
        pass

    def get_value(self, id, field):
        pass

    def get_values(self, id):
        pass

    def set_values(self, id):
        pass

    def stream(self) -> Stream:
        return Stream(self, self.__stream_url)

    def __get(self, url, is_json=True, **kwargs) -> Any:
        resp = requests.get(url, headers=self.__get_headers(), **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__get(url, is_json=is_json, **kwargs)
        return None

    def __post(self, url, data: Any, is_json=True, **kwargs) -> Any:
        if is_json:
            resp = requests.post(url, json=data, headers=self.__get_headers(), **kwargs)
        else:
            resp = requests.post(url, data=data, headers=self.__get_headers(), **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__post(url, data=data, is_json=is_json, **kwargs)
        return None

    def __put(self, url, data: Any, is_json=True, **kwargs) -> Any:
        if is_json:
            resp = requests.post(url, json=data, headers=self.__get_headers(), **kwargs)
        else:
            resp = requests.post(url, data=data, headers=self.__get_headers(), **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__put(url, data=data, is_json=is_json, **kwargs)
        return None

    def __delete(self, url, is_json=True, **kwargs) -> Any:
        resp = requests.delete(url, headers=self.__get_headers(), **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__delete(url, is_json=is_json, **kwargs)
        return None

    def __refresh(self):
        resp = requests.post(f'{self.__app_url}/user/refresh', json={
            'userId': self.__user_id,
            'refreshToken': self.__refresh_token,
        })

        if resp.status_code != 200:
            return False

        login_info = resp.json()
        self.__access_token = login_info['accessToken']

        return True

    def __request_permission(self, req):
        if req == 'token expired':
            return self.__refresh()

        perm_reqs = req.split('/')
        if perm_reqs[0] == '00000000000000000000000000000000':
            return False

        tk = self.__space_tokens.get(perm_reqs[0])
        if tk is not None:
            return False

        perms = int(perm_reqs[1], 16)

        resp = self.__get(f'{self.__app_url}/permission/{perm_reqs[0]}')
        if (perms & resp['perms']) != perms:
            return False

        self.__space_tokens[req] = resp

        return True

    def __get_headers(self, cached=False):
        return {
            'Authorization': f'Baerer {self.__access_token}',
            'x-vy-spaces': ','.join([v['token'] for (k, v) in self.__space_tokens.items()]),
            'x-vy-bypass-cache': '1' if cached else '0',
        }
