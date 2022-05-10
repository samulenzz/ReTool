import json
import pytest
import requests

from requirementmanager.api.requirement.edit import META_SUCCESS, META_ERROR_NO_REQUIREMENT, META_ERROR_NO_ACCESS

from .config import BASE_URL

url = f"{BASE_URL}/requirement/edit"


class TestRequirementEdit:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_requirement_create import create_test_requirement
        
        self.requirement_id = create_test_requirement()

    def test_edit_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {
            "requirement_id": "a5ac042ed05d11ecb9393c7c3f2b2c02",
            "name": "添加xxx",
            "description": "111222333444"
        }
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.8-1')

    def test_project_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"requirement_id": -1}
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_REQUIREMENT
        print('4.3.8-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {
            "requirement_id": "a5ac042ed05d11ecb9393c7c3f2b2c02",
            "name": "添加xxx",
            "description": "111222333444"
        }
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_ACCESS
        print('4.3.8-3')

    def teardown_class(self):
        from .test_requirement_delete import delete_test_requirement
        delete_test_requirement(self.requirement_id)


if __name__ == '__main__':
    pytest.main()
