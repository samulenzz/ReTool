from flask import request

from usermanager.app import app
from usermanager.dao.user import (
    User, UserMongoDBDao
)
from usermanager.mongodb import user_collection
from usermanager.utils.handle_api import verify_system_role, handle_response
from usermanager.utils.password import encrypt_password


META_SUCCESS = {'status': 200, 'msg': '添加成功！'}
META_ERROR = {'status': 400, 'msg': '添加失败！该用户已存在！'}


@app.route('/user/create', methods=['POST'])
@handle_response
@verify_system_role
def user_create():
    body = request.json
    user_mongodb_dao = UserMongoDBDao(user_collection)
    # Check if user exists
    if user_mongodb_dao.get_user(body['username']):
        return {'meta': META_ERROR}
    # Encrypt password
    body['password'] = encrypt_password(body['password'])
    user = User(**body)
    user_mongodb_dao.create_user(user)
    return {'meta': META_SUCCESS}
