import json
import pytest
import requests

from usermanager.api.user.profile import META_SUCCESS, META_ERROR
from usermanager.utils.handle_api import META_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/user/profile"


class TestUserProfile:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.admin_token is not None

    def test_get_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "liuzh"}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.5-1')

    def test_username_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "不存在用户"}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.1.5-2')


if __name__ == '__main__':
    pytest.main()
