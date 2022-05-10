import json
import pytest
import requests

from usermanager.api.register import META_SUCCESS, META_ERROR

from .config import BASE_URL

url = f"{BASE_URL}/register"


class TestRegister:

    def setup_class(self):
        pass

    def test_register_successful(self):
        payload = {"username": "liuzehua", "password": "123456", 'system_role': '普通用户'}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.7-1')

    def test_username_exist(self):
        payload = {"username": "admin", "password": "123456", 'system_role': '普通用户'}
        r = requests.post(url, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.7-2')

    def teardown_class(self):
        from .test_user_delete import delete_test_user
        delete_test_user('liuzehua')


if __name__ == '__main__':
    pytest.main()
