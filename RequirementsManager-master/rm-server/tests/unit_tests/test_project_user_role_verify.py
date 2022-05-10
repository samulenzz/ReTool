import json
import pytest
import requests

from projectmanager.api.project.user.role.verify import META_SUCCESS
from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/project/user/role/verify"


class TestProjectUserRoleVerify:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_project_create import create_test_project
        self.project_id = create_test_project()

    def test_inner_interface_access(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": self.project_id, 'username': 'admin', 'access': 'project_edit'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 404
        print('4.2.8-1')

    def teardown_class(self):
        from .test_project_delete import delete_test_project
        delete_test_project(self.project_id)


if __name__ == '__main__':
    pytest.main()
