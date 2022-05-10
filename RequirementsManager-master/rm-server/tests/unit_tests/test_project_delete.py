import json
import pytest
import requests

from projectmanager.api.project.delete import META_SUCCESS
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/delete"


def delete_test_project(project_id):
    from .test_login import login
    admin_token = login(admin=True)
    assert admin_token is not None
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"project_id": project_id}
    r = requests.delete(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS


class TestProjectDelete:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_project_create import create_test_project
        self.project_id1 = create_test_project()

        test_project_users = [{'username': 'admin', 'project_role': '项目经理'},
                              {'username': 'liuzh', 'project_role': '普通成员'}]
        self.project_id2 = create_test_project(users=test_project_users)

    def test_delete_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": self.project_id1}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.2.2-1')

    def test_project_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": -1}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_PROJECT
        print('4.2.2-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"project_id": self.project_id2}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_ACCESS
        print('4.2.2-3')

    def teardown_class(self):
        delete_test_project(self.project_id2)


if __name__ == '__main__':
    pytest.main()
