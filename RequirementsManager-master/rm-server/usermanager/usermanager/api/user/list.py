from flask import request
from urllib.parse import unquote

from usermanager.app import app
from usermanager.dao.user import UserMongoDBDao
from usermanager.dao.user_list import (
    UserListMongoDBDao
)
from usermanager.mongodb import user_collection
from usermanager.utils.handle_api import handle_response

from usermanager.dao.user import SYSTEM_ROLE_SYSTEM_MANAGER

META_SUCCESS = {'status': 200, 'msg': '成功！'}


@app.route('/user/list', methods=['GET'])
@handle_response
def user_list():
    # 检查操作用户的用户角色
    client_username = request.headers.get('Client-Username')
    # 对Headers中的中文进行解码
    client_username = unquote(client_username)
    user_mongodb_dao = UserMongoDBDao(user_collection)
    client_user = user_mongodb_dao.get_user(client_username)
    if client_user.system_role != SYSTEM_ROLE_SYSTEM_MANAGER:
        tmp_user = client_user.jsonify()
        tmp_user.pop('password')
        data = [tmp_user]
        return {
            'data': data,
            'meta': META_SUCCESS
        }

    # 获取所有用户信息
    user_list_mongodb_dao = UserListMongoDBDao(user_collection)
    users = user_list_mongodb_dao.get_all_users()
    data = []
    for user in users:
        tmp_user = user.jsonify()
        tmp_user.pop('password')
        data.append(tmp_user)
    return {
        'data': data,
        'meta': META_SUCCESS
    }
