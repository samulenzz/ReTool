import json
import pytest
import requests

from usermanager.api.user.delete import META_SUCCESS, META_ERROR
from usermanager.utils.handle_api import META_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/user/delete"


def delete_test_user(username='liuzehua'):
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": username}
    r = requests.delete(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS


class TestUserDelete:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.admin_token is not None

        from .test_user_create import create_test_user
        create_test_user()

    def test_delete_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzehua"}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.2-1')

    def test_username_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzehua"}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.2-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"username": "liuzehua"}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_NO_ACCESS
        print('4.1.2-3')


if __name__ == '__main__':
    pytest.main()
