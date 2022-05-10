import json
import pytest
import requests

from requirementmanager.api.requirement.importfile.itemize import META_SUCCESS, META_ERROR_NO_FILE

url = f"http://10.132.18.124:8080/requirement/importfile/itemize"

def itemsize():
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {'token': '769785a4d03e11ec93de3c7c3f2b2c02'}
    r = requests.post(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    return results['data']

class TestRequirementItemsize:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_itemsize_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {'token': '769785a4d03e11ec93de3c7c3f2b2c02'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.4-1')

    def test_itemsizet_not_exist(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        payload = {'token': '1'}
        r = requests.post(url, headers=headers, json=payload)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_NO_FILE
        print('4.3.4-2')

if __name__ == '__main__':
    pytest.main()