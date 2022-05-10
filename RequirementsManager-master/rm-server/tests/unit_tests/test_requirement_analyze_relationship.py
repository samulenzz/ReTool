import json
import pytest
import requests

from requirementmanager.api.requirement.analyze.relationship import META_SUCCESS

url = f"http://10.132.18.124:8080/requirement/analyze/relationship"

class TestRequirementAnalyzeRelationship:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_TestRequirementAnalyzeRelationship_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {
            "scope": {
                "project_id": "366c2e11d05911ec91913c7c3f2b2c02",
                "version": None
            },
            "target_type": "edit_single",
            "target_data": {
                "_id": "a5ac042ed05d11ecb9393c7c3f2b2c02",
                "name": "添加xxx",
                "description": "111222333444",
                "_type": "2"
            }
        }
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.12-1')

if __name__ == '__main__':
    pytest.main()