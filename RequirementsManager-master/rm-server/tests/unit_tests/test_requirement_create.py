import json
import pytest
import requests

from requirementmanager.api.requirement.create import META_SUCCESS
from requirementmanager.utils.handle_api import META_ERROR_NO_ACCESS


url = f"http://10.132.18.124:8080/requirement/create"


def create_test_requirement():
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {
                "project_id": "366c2e11d05911ec91913c7c3f2b2c02",
                "base_id": "3",
                "location": "inner",
                "name": "添加用户",
                "description": "为系统添加用户",
                "status": "进行中",
                "priority": "高",
                "expected_start_time": "2022-04-30T16:00:00.000Z",
                "expected_end_time": "2022-05-10T16:00:00.000Z"
    }
    r = requests.post(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    return results['data']['requirement_id']

def create_test_requirement2():
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {
            "project_id": "366c2e11d05911ec91913c7c3f2b2c02",
            "base_id": "3",
            "location": "inner",
            "name": "安全",
            "description": "安全要求",
            "status": "进行中",
            "priority": "高",
            "expected_start_time": "2022-05-13T16:00:00.000Z",
            "expected_end_time": "2022-05-15T16:00:00.000Z"
    }
    r = requests.post(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    return results['data']['requirement_id']


class TestRequirementCreate:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_create_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {
                "project_id": "366c2e11d05911ec91913c7c3f2b2c02",
                "base_id": "3",
                "location": "inner",
                "name": "添加用户",
                "description": "为系统添加用户",
                "status": "进行中",
                "priority": "高",
                "expected_start_time": "2022-04-30T16:00:00.000Z",
                "expected_end_time": "2022-05-10T16:00:00.000Z"
        }
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.1-1')
        # teardown_class
        # from .test_project_delete import delete_test_project
        # delete_test_project(results['project_id'])


if __name__ == '__main__':
    pytest.main()
    # create_test_requirement()
