import json
import pytest
import requests

from requirementmanager.api.requirement.importfile.upload import META_SUCCESS, META_ERROR_BAD_FILE


url = f"http://10.132.18.124:8080/requirement/importfile/upload"

# def login(admin=True):
#     if admin:
#         payload = {"username": "admin", "password": "123456"}
#         r = requests.post(f'http://10.132.18.124:8080/login', json=payload)
#         assert r.status_code == 200
#         results = json.loads(r.content)
#         assert results['meta'] == {'status': 200, 'msg': '登录成功！'}
#         return results['data']['token']
#     else:
#         payload = {"username": "liuzh", "password": "123456"}
#         r = requests.post(url, json=payload)
#         assert r.status_code == 200
#         results = json.loads(r.content)
#         # assert results['meta'] == META_SUCCESS
#         return results['data']['token']

def upload_test_doc():
    from .test_login import login
    admin_token = login(admin=True)
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    myfile = {'file': open('/home/nzz/样例需求文档三.docx', 'rb')}
    r = requests.post(url, headers=headers, files=myfile)
    assert r.status_code == 200
    results = json.loads(r.content)
    print(results)
    assert results['meta'] == META_SUCCESS
    return results['data']['token']

class TestRequirementUpload:

    def setup_class(self):
        from .test_login import login
        self.admin_token = login(admin=True)
        assert self.admin_token is not None

    def test_upload_successful(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        myfile = {'file': open('/home/nzz/样例需求文档三.docx', 'rb')}
        r = requests.post(url, headers=headers, files=myfile)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_SUCCESS
        print('4.3.2-1')

    def test_upload_fail(self):
        headers = {"Client-Username": "admin", "Authorization": self.admin_token}
        myfile = {'file': open('/home/nzz/111.txt', 'rb')}
        r = requests.post(url, headers=headers, files=myfile)
        assert r.status_code == 200
        results = json.loads(r.content)
        assert results['meta'] == META_ERROR_BAD_FILE
        print('4.3.2-2')


if __name__ == '__main__':
    pytest.main()
    # upload_test_doc()