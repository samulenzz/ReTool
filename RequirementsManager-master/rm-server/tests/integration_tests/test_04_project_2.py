import json
import pytest
import requests
from .config import BASE_URL
from usermanager.api.login import META_SUCCESS as LOGIN_SUCCESS
from projectmanager.api.project.create import META_SUCCESS as PROJECT_CREATE_SUCCESS
from projectmanager.api.project.profile import META_SUCCESS as PROJECT_PROFILE_SUCCESS
from projectmanager.api.project.edit import META_SUCCESS as PROJECT_EDIT_SUCCESS
from projectmanager.api.project.delete import META_SUCCESS as PROJECT_DELETE_SUCCESS
from projectmanager.api.project.user.edit import META_SUCCESS as PROJECT_USER_EDIT_SUCCESS
from projectmanager.api.project.baseline.node.create import META_SUCCESS as PROJECT_BASELINE_CREATE_SUCCESS
from requirementmanager.api.requirement.create import META_SUCCESS as REQ_CREATE_SUCCESS

token = ""
project_id = ""


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
    r = requests.delete(BASE_URL + "/project/delete", headers = headers, json = payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_DELETE_SUCCESS
    # print("删除成功")

def create_test_requirement():
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
    r = requests.post(BASE_URL + "/requirement/create", headers = headers, json = payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == REQ_CREATE_SUCCESS

def setup_function():
    login()
    create_test_project()


def teardown_function():
    delete_test_project()


def test_project_1():
    # 测试步骤1，展示项目信息
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id}
    r = requests.get(BASE_URL + "/project/profile", headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_PROFILE_SUCCESS
    print('\n4.4-1 展示项目信息测试通过')

    # 测试步骤2，更新项目信息
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id,
               "project_name": "alter_test",
               "description": "修改后的信息",
               "status": "进行中"}
    r = requests.put(BASE_URL + "/project/edit", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_EDIT_SUCCESS
    print('4.4-2 更新项目信息测试通过')

    # 测试步骤3，修改项目成员
    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id,
               'users': [{'username': 'admin', 'project_role': '项目经理'}, {'username': '李四', 'project_role': '项目组长'}]}
    r = requests.put(BASE_URL + "/project/user/edit", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_USER_EDIT_SUCCESS

    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id,
               'users': [{'username': 'admin', 'project_role': '项目经理'}]}
    r = requests.put(BASE_URL + "/project/user/edit", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_USER_EDIT_SUCCESS

    print('4.4-3 修改项目成员测试通过')

    # 测试步骤4，创建基线节点
    # 先添加一个需求
    create_test_requirement()

    headers = {"Client-Username": "admin", "Authorization": token}
    payload = {"project_id": project_id, 'name': 'v1.0', 'description': '版本1.0'}
    r = requests.post(BASE_URL + "/project/baseline/node/create", headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == PROJECT_BASELINE_CREATE_SUCCESS
    print('4.4-4 创建基线节点测试通过')


if __name__ == '__main__':
    pytest.main(["test_04_project_2.py", "-s"])
