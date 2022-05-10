import json
import pytest
import requests

from projectmanager.api.project.create import META_SUCCESS
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/create"


def create_test_project(project_name='Test_Project', description='Only for test.', status='未开始', users=None):
    if users is None:
        users = [{'username': 'admin', 'project_role': '项目经理'}]
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"project_name": project_name, "description": description, "status": status, "users": users}
    r = requests.post(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    return results['project_id']


class TestProjectCreate:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_create_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_name": "Test_Project", "description": "Only for test.", "status": "未开始",
                   "users": [{'username': 'admin', 'project_role': '项目经理'}]}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.2.1-1')
        # teardown_class
        from .test_project_delete import delete_test_project
        delete_test_project(results['project_id'])


if __name__ == '__main__':
    pytest.main()
