import json
import pytest
import requests

from usermanager.api.user.edit import META_SUCCESS, META_ERROR
from usermanager.utils.handle_api import META_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/user/edit"


class TestUserEdit:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.admin_token is not None

        from .test_user_create import create_test_user
        create_test_user()

    def test_edit_password_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzehua", "password": "12345678"}
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.3-1')

    def test_edit_system_role_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzehua", "system_role": "系统管理员"}
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.3-2')

    def test_username_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "不存在用户", "password": "12345678", "system_role": "系统用户"}
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.3-3')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"username": "liuzehua", "password": "123456"}
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_NO_ACCESS
        print('4.1.3-4')

    def teardown_class(self):
        from .test_user_delete import delete_test_user
        delete_test_user()


if __name__ == '__main__':
    pytest.main()
