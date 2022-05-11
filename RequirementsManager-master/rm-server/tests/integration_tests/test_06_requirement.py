import json
import pytest
import requests
from config import BASE_URL
from usermanager.api.login import META_SUCCESS as LOGIN_SUCCESS
from projectmanager.api.project.create import META_SUCCESS as PROJECT_CREATE_SUCCESS
from projectmanager.api.project.delete import META_SUCCESS as PROJECT_DELETE_SUCCESS
from requirementmanager.api.requirement.importfile.upload import META_SUCCESS as REQ_IMPORTFILE_SUCCESS
from requirementmanager.api.requirement.importfile.itemize import META_SUCCESS as REQ_ITEMIZE_SUCCESS
from requirementmanager.api.requirement.analyze.conflict import META_SUCCESS as REQ_CONFLICT_SUCCESS
from requirementmanager.api.requirement.analyze.similarity import META_SUCCESS as REQ_SIMILARITY_SUCCESS
from requirementmanager.api.requirement.analyze.relationship import META_SUCCESS as REQ_RELATIONSHIP_SUCCESS

token = ""
project_id = ""
file_token = ""

def login(admin=True):
    global token
    payload = {"username": "admin", "password": "123456"}
    r = requests.post(BASE_URL + "/login", json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == LOGIN_SUCCESS
    token = results['data']['token']


def create_test_project(project_name='Test_Project', description='Only for test.', status='未开始', users=None):
    global project_id
    if users is None:
        users = [{'username': 'admin', 'project_role': '项目经理'}]
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_name": project_name, "description": description, "status": status, "users": users}
    r = requests.post(BASE_URL + "/project/create", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_CREATE_SUCCESS
    project_id = results['project_id']


def delete_test_project():
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id}
    r = requests.delete(BASE_URL + "/project/delete", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_DELETE_SUCCESS

def setup_function():
    login()
    create_test_project()

def teardown_function():
    delete_test_project()

def test_requirement_2():
    # 测试步骤1，上传文档
    headers = {"Client-Username": "admin", "Authorization": token}
    myfile = {'file': open(r'C:\Users\wang9\Desktop\软工实验\样例需求文档三.docx', 'rb')}
    r = requests.post(BASE_URL + "/requirement/importfile/upload", headers=headers, files=myfile)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_IMPORTFILE_SUCCESS
    file_token = results['data']['token']
    print('\n4.6-1 上传文档测试通过')

    # 测试步骤2，需求文档条目化
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {'token': file_token}
    r = requests.post(BASE_URL + "/requirement/importfile/itemize", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_ITEMIZE_SUCCESS
    req_tree = results['data']
    print('4.6-2 需求文档条目化测试通过')

    # 测试步骤3，冲突检测
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "scope": {
            "project_id": project_id,
            "version": None
        },
        "target_type": "tree",
        "target_data": req_tree
    }
    r = requests.post(BASE_URL + "/requirement/analyze/conflict", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_CONFLICT_SUCCESS
    print('4.6-3 需求文档冲突检测通过')

    # 测试步骤4，共性识别
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "scope": {
            "project_id": project_id,
            "version": None
        },
        "target_type": "tree",
        "target_data": req_tree
    }
    r = requests.post(BASE_URL + "/requirement/analyze/similarity", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_SIMILARITY_SUCCESS
    print('4.6-4 需求文档共性识别通过')

    # 测试步骤5，关联关系检测
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "scope": {
            "project_id": project_id,
            "version": None
        },
        "target_type": "tree",
        "target_data": req_tree
    }
    r = requests.post(BASE_URL + "/requirement/analyze/relationship", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_RELATIONSHIP_SUCCESS
    print('4.6-5 需求文档关联关系检测通过')



if __name__ == '__main__':
    pytest.main(["test_06_requirement.py", "-s"])