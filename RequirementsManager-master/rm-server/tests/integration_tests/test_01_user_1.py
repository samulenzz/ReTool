import json
import pytest
import requests

from .config import BASE_URL

admin_token = ""
liuzh_token = ""
"""
def setup_function():
    global admin_token
    global liuzh_token
    from test_login import login

    # 测试用户
    new_user.admin_token = login(admin=True)
    assert admin_token is not None

    new_user.liuzh_token = login(admin=False)
    assert liuzh_token is not None


    # # logger.info("setup success")
    print("setup success")
"""


def test_integration_01():
    '''
    集成测试：用户登录登出及查看修改基本信息集成测试
    '''
    # logger.info("集成测试01: 用户登录登出及查看修改基本信息集成测试")
    print("集成测试01: 用户登录登出及查看修改基本信息集成测试")

    ''' Step1 用户登录 '''
    # logger.info("Step1: "+"用户登录")
    print("Step1: " + "用户登录")

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
    url = f"{BASE_URL}/login"
    from usermanager.api.login import META_SUCCESS, META_ERROR
    from tests.unit_tests.test_login import login
    payload = {"username": "admin", "password": "123456"}
    r = requests.post(url, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    """

    ''' Step2 查看个人信息 '''
    # logger.info("Step2: "+"查看个人信息")
    print("Step2: " + "查看个人信息")
    url = f"{BASE_URL}/user/profile"
    from usermanager.api.user.profile import META_SUCCESS, META_ERROR
    from usermanager.utils.handle_api import META_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": "liuzh"}
    r = requests.get(url, headers=headers, params=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS

    ''' Step3 修改个人信息:修改密码/修改用户角色'''
    # logger.info("Step3: "+"修改个人信息")
    print("Step3: " + "修改个人信息")
    url = f"{BASE_URL}/user/edit"
    from usermanager.api.user.edit import META_SUCCESS, META_ERROR
    from usermanager.utils.handle_api import META_NO_ACCESS
    from ..unit_tests.test_user_create import create_test_user
    create_test_user()
    # password
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": "liuzehua", "password": "12345678"}
    r = requests.put(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    # system_role
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    payload = {"username": "liuzehua", "system_role": "系统管理员"}
    r = requests.put(url, headers=headers, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    # teardown
    from ..unit_tests.test_user_delete import delete_test_user
    delete_test_user()


if __name__ == '__main__':
    pytest.main(["test_01_user_1.py", "-s"])