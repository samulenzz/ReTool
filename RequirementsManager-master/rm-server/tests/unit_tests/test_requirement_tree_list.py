import json
import pytest
import requests

from requirementmanager.api.requirement.tree.list import META_SUCCESS

from .config import BASE_URL

url = f"{BASE_URL}/requirement/tree/list"

class TestTreeList:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_tree_list_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {"project_id": "366c2e11d05911ec91913c7c3f2b2c02",}
        r = requests.get(url, headers=headers, params=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.6-1')


if __name__ == '__main__':
    pytest.main()