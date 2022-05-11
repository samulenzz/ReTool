import json
import pytest
import requests

from .config import BASE_URL

admin_token=""
liuzh_token=""
project_id=""
"""
def setup_function():
    global new_user
    from tests.unit_tests.test_login import login
    # 测试用户
    new_user.admin_token = login(admin=True)
    assert new_user.admin_token is not None

    new_user.liuzh_token = login(admin=False)
    assert new_user.liuzh_token is not None

    print("setup success")
"""

def test_integration_01():
    '''
    集成测试：项目增删查功能集成测试
    '''
    print("集成测试03: 项目增删查功能集成测试")
    
    
    ''' Step1 用户登录 '''
    
    print("Step1: "+"用户登录")
    
    global admin_token
    global liuzh_token
    from ..unit_tests.test_login import login
    
    # 测试用户
    admin_token = login(admin=True)
    assert admin_token is not None

    liuzh_token = login(admin=False)
    assert liuzh_token is not None

    
    # logger.info("setup success")
    print("setup success")
    """
    print("Step1: "+"用户登录")
    url = f"{BASE_URL}/login"
    from usermanager.api.login import META_SUCCESS, META_ERROR
    from test_login import login
    payload = {"username": "admin", "password": "123456"}
    r = requests.post(url, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    """
    
    ''' Step2 显示项目列表 '''
    print("Step2: "+"项目列表")
    url = f"{BASE_URL}/project/list"
    from projectmanager.api.project.list import META_SUCCESS
    from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": "admin"}
    r = requests.get(url, headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    
    
    ''' Step3 创建项目'''
    print("Step3: "+"创建项目")
    from ..unit_tests.test_project_create import create_test_project
    test_project_users = [{'username': 'admin', 'project_role': '项目经理'},
                          {'username': 'liuzh', 'project_role': '普通成员'}]
    global project_id
    project_id = create_test_project(users=test_project_users)


    
    ''' Step4 显示项目信息'''
    print("Step4: "+"显示项目信息")
    # 基本信息
    url = f"{BASE_URL}/project/profile"
    from projectmanager.api.project.profile import META_SUCCESS
    from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"project_id": project_id}
    r = requests.get(url, headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    # 本项目成员列表
    url = f"{BASE_URL}/project/user/list"
    from projectmanager.api.project.user.list import META_SUCCESS
    from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"project_id": project_id}
    r = requests.get(url, headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    # 项目基线节点列表
    url = f"{BASE_URL}/project/baseline/node/list"
    from projectmanager.api.project.baseline.node.list import META_SUCCESS
    from projectmanager.utils.handle_api import META_ERROR_NO_PROJECT, META_ERROR_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"project_id": project_id}
    r = requests.get(url, headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    
    
    ''' Step5 删除项目'''
    print("Step4: "+"删除项目")
    from ..unit_tests.test_project_delete import delete_test_project
    delete_test_project(project_id)

if __name__ == '__main__':
    pytest.main(["test_03_project_1.py", "-s"])