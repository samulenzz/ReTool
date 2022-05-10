import json
import pytest
import requests

from requirementmanager.api.requirement.delete import META_SUCCESS, META_ERROR_NO_REQUIREMENT, META_ERROR_NO_ACCESS

url = f"http://10.132.18.124:8080/requirement/delete"


def delete_test_requirement(requirement_id):
    from .test_login import login
    admin_token = login(admin=True)
    assert admin_token is not None
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"requirement_id": requirement_id}
    r = requests.delete(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS


class TestRequirementDelete:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

        self.liuzh_token = login(admin=False)
        assert self.liuzh_token is not None

        from .test_requirement_create import create_test_requirement, create_test_requirement2
        self.requirement_id1 = create_test_requirement()

        self.requirement_id2 = create_test_requirement2()

    def test_delete_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"requirement_id": self.requirement_id1}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.7-1')

    def test_requirement_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"requirement_id": -1}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_REQUIREMENT
        print('4.3.7-2')

    def test_system_role(self):
        headers = {"Client-Username": "liuzh", "Authorization": self.liuzh_token}
        payload = {"requirement_id": self.requirement_id2}
        r = requests.delete(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_ACCESS
        print('4.3.7-3')

    def teardown_class(self):
        delete_test_requirement(self.requirement_id2)


if __name__ == '__main__':
    pytest.main()
