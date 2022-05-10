import json
import pytest
import requests

from projectmanager.api.project.baseline.node.create import META_SUCCESS, META_ERROR
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/baseline/node/create"


class TestProjectBaselineNodeCreate:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_project_create import create_test_project
        test_project_users = [{'username': 'admin', 'project_role': '项目经理'},
                              {'username': 'liuzh', 'project_role': '普通成员'}]
        self.project_id = create_test_project(users=test_project_users)

    def test_create_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": "cf0cce1bd00d11ecb9c73c7c3f2b2c02", 'name': 'v1.0', 'description': '需求1.0'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.2.9-1')

    def test_project_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": -1}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_PROJECT
        print('4.2.9-2')

    def test_requirement_empty(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": self.project_id, 'name': 'v1.0', 'description': '需求1.0'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR
        print('4.2.9-3')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"project_id": self.project_id, 'name': 'v1.0', 'description': '需求1.0'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_ACCESS
        print('4.2.9-4')

    def teardown_class(self):
        from .test_project_delete import delete_test_project
        delete_test_project(self.project_id)


if __name__ == '__main__':
    pytest.main()
