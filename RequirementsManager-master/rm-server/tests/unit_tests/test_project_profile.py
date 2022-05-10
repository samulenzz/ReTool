import json
import pytest
import requests

from projectmanager.api.project.profile import META_SUCCESS
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/profile"


class TestProjectProfile:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_project_create import create_test_project
        self.project_id = create_test_project()

    def test_profile_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": self.project_id}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.2.5-1')

    def test_project_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": -1}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_PROJECT
        print('4.2.5-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"project_id": self.project_id}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_ACCESS
        print('4.2.5-3')

    def teardown_class(self):
        from .test_project_delete import delete_test_project
        delete_test_project(self.project_id)


if __name__ == '__main__':
    pytest.main()
