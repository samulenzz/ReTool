import json
import pytest
import requests

from usermanager.api.user.create import META_SUCCESS, META_ERROR
from usermanager.utils.handle_api import META_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/user/create"


def create_test_user(username='liuzehua', password='123456', system_role='系统用户'):
    from .test_login import login
    admin_token = login(admin=True)
    assert admin_token is not None
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": username, "password": password, "system_role": system_role}
    r = requests.post(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS


class TestUserCreate:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.admin_token is not None

    def test_create_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzehua", "password": "123456", "system_role": "系统用户"}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.1-1')

    def test_username_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "admin", "password": "123456", "system_role": "系统用户"}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.1-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"username": "liuzehua", "password": "123456", "system_role": "系统用户"}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_NO_ACCESS
        print('4.1.1-3')

    def teardown_class(self):
        from .test_user_delete import delete_test_user
        delete_test_user()


if __name__ == '__main__':
    pytest.main()
