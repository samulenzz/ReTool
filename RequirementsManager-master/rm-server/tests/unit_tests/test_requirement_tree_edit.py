import json
import pytest
import requests

from requirementmanager.api.requirement.tree.edit import META_SUCCESS

from .config import BASE_URL

url = f"{BASE_URL}/requirement/tree/edit"

class TestRequirementTreeEdit:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_RequirementTreeEdit_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {
            "project_id": "366c2e11d05911ec91913c7c3f2b2c02",
            "requirement_id": "a1bd3092d05f11ecb73d3c7c3f2b2c02",
            "base_id": "7",
            "location": "inner"
        }
        r = requests.put(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.9-1')

if __name__ == '__main__':
    pytest.main()