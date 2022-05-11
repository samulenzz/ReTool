import json
import pytest
import requests
from .config import BASE_URL
from usermanager.api.login import META_SUCCESS as LOGIN_SUCCESS
from projectmanager.api.project.create import META_SUCCESS as PROJECT_CREATE_SUCCESS
from projectmanager.api.project.delete import META_SUCCESS as PROJECT_DELETE_SUCCESS
from requirementmanager.api.requirement.tree.list import META_SUCCESS as REQ_TREE_LIST_SUCCESS
from requirementmanager.api.requirement.tree.edit import META_SUCCESS as REQ_TREE_EDIT_SUCCESS
from requirementmanager.api.requirement.create import META_SUCCESS as REQ_CREATE_SUCCESS
from requirementmanager.api.requirement.edit import META_SUCCESS as REQ_EDIT_SUCCESS
from requirementmanager.api.requirement.delete import META_SUCCESS as REQ_DELETE_SUCCESS

token = ""
project_id = ""
req_id = ""


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

def create_test_requirement():
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "project_id": project_id,
        "base_id": "3",
        "location": "inner",
        "name": "添加用户1",
        "description": "为系统添加用户1",
        "status": "进行中",
        "priority": "高",
        "expected_start_time": "2022-04-30T16:00:00.000Z",
        "expected_end_time": "2022-05-10T16:00:00.000Z"
    }
    r = requests.post(BASE_URL + "/requirement/create", headers = headers, json = payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_CREATE_SUCCESS

    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "project_id": project_id,
        "base_id": "3",
        "location": "inner",
        "name": "添加用户2",
        "description": "为系统添加用户2",
        "status": "进行中",
        "priority": "高",
        "expected_start_time": "2022-04-30T16:00:00.000Z",
        "expected_end_time": "2022-05-10T16:00:00.000Z"
    }
    r = requests.post(BASE_URL + "/requirement/create", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_CREATE_SUCCESS

def setup_function():
    login()
    create_test_project()
    create_test_requirement()

def teardown_function():
    delete_test_project()


def test_requirement_1():
    global req_id
    # 测试步骤1，展示需求条目树
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id, }
    r = requests.get(BASE_URL + "/requirement/tree/list", headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_TREE_LIST_SUCCESS
    print('\n4.5-1 展示需求条目树通过')

    # 测试步骤234，添加子需求
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "project_id": project_id,
        "base_id": "3",
        "location": "inner",
        "name": "添加用户",
        "description": "为系统添加用户",
        "status": "进行中",
        "priority": "高",
        "expected_start_time": "2022-04-30T16:00:00.000Z",
        "expected_end_time": "2022-05-10T16:00:00.000Z"
    }
    r = requests.post(BASE_URL + "/requirement/create", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_CREATE_SUCCESS
    req_id = results['data']['requirement_id']
    print('4.5-234 添加子需求通过')

    # 测试步骤5，移动需求
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "project_id": project_id,
        "base_id": "3",
        "location": "inner",
        'requirement_id': req_id
    }
    r = requests.put(BASE_URL + "/requirement/tree/edit", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_TREE_EDIT_SUCCESS
    print('4.5-5 移动需求通过')

    # 测试步骤6，修改需求
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {
        "requirement_id": req_id,
        "name": "被改变的需求",
        "description": "test"
    }
    r = requests.put(BASE_URL + "/requirement/edit", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_EDIT_SUCCESS
    print('4.5-6 修改需求通过')

    # 测试步骤7，删除需求
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"requirement_id": req_id}
    r = requests.delete(BASE_URL + "/requirement/delete", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_DELETE_SUCCESS
    print('4.5-7 删除需求通过')



if __name__ == '__main__':
    pytest.main(["test_05_requirement.py", "-s"])
