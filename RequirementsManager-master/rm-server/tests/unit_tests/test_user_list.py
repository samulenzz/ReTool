import json
import pytest
import requests

from usermanager.api.user.list import META_SUCCESS
from usermanager.utils.handle_api import META_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/user/list"


class TestUserList:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.admin_token is not None

    def test_admin_get_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        r = requests.get(url, headers=headers)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.1.4-1')

    def test_liuzh_get_successful(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        r = requests.get(url, headers=headers)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        assert len(results['data']) == 1
        assert results['data'][0]['username'] == 'liuzh'
        print('4.1.4-2')

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main()
