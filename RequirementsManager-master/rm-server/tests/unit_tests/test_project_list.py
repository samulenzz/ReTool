import json
import pytest
import requests

from projectmanager.api.project.list import META_SUCCESS
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/list"


class TestProjectList:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_list_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"username": "admin"}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.2.4-1')

    def teardown_class(self):
        pass


if __name__ == '__main__':
    pytest.main()
