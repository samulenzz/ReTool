import json
import pytest
import requests

from .config import BASE_URL

admin_token=""
liuzh_token=""

"""
def setup_function():
    global new_user
    from tests.unit_tests.test_login import login
    # 测试用户
    new_user.admin_token = login(admin=True)
    assert new_user.admin_token is not None

    new_user.liuzh_token = login(admin=False)
    assert new_user.liuzh_token is not None

    logger.info("setup success")
"""

def test_integration_02():
    '''
    集成测试：管理员添加用户和重置用户信息集成测试
    '''
    print("集成测试02: 管理员添加用户和重置用户信息集成测试")
    
    
    ''' Step1 管理员登录 '''
    print("Step1: "+"管理员登录")
    
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
    logger.info("Step1: "+"管理员登录")
    url = f"{BASE_URL}/login"
    from usermanager.api.login import META_SUCCESS, META_ERROR
    from tests.unit_tests.test_login import login
    payload = {"username": "admin", "password": "123456"}
    r = requests.post(url, json=payload)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    """


    ''' Step2 显示用户列表 '''
    # logger.info("Step2: "+"显示用户列表")
    print("Step2: "+"显示用户列表")
    url = f"{BASE_URL}/user/list"
    from usermanager.api.user.list import META_SUCCESS
    from usermanager.utils.handle_api import META_NO_ACCESS
    headers = {"Client-Username": "admin", "Authorization": admin_token}
    r = requests.get(url, headers=headers)
    assert r.status_code == 200
    results = json.loads(r.content)
    assert results['meta'] == META_SUCCESS
    
    
    ''' Step3 添加用户'''
    # logger.info("Step3: "+"添加用户")
    print("Step3: "+"添加用户")
    url = f"{BASE_URL}/user/create"
    from usermanager.api.user.create import META_SUCCESS, META_ERROR
    from usermanager.utils.handle_api import META_NO_ACCESS
    from ..unit_tests.test_user_create import create_test_user
    create_test_user()

    
    ''' Step4 修改个人信息'''
    print("Step4: "+"修改个人信息")
    url = f"{BASE_URL}/user/edit"
    from usermanager.api.user.edit import META_SUCCESS, META_ERROR
    from usermanager.utils.handle_api import META_NO_ACCESS
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
    
    ''' Step5 删除用户'''
    print("Step4: "+"删除用户")
    from ..unit_tests.test_user_delete import delete_test_user
    delete_test_user()

if __name__ == '__main__':
    pytest.main(["test_02_user_2.py", "-s"])