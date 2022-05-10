import json
import pytest
import requests

from usermanager.api.login import META_SUCCESS, META_ERROR

from .config import BASE_URL

url = f"{BASE_URL}/login"


def login(admin=True):
    if admin:
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        return results['data']['token']
    else:
        payload = {"username": "liuzh", "password": "123456"}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        return results['data']['token']


class TestLogin:

    def setup_class(self):
        pass

    def test_login_successful(self):
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.6-1')

    def test_username_not_exist(self):
        payload = {"username": "liuzehua", "password": "123456"}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.6-2')

    def test_password_wrong(self):
        payload = {"username": "admin", "password": "1234567"}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.6-3')

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main()
