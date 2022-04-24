from flask import request

from usermanager.app import app
from usermanager.dao.user import UserMongoDBDao
from usermanager.mongodb import user_collection
from usermanager.utils.handle_api import (
    verify_edit_user_request, handle_response
)
from usermanager.utils.password import encrypt_password

META_SUCCESS = {'status': 200, 'msg': '修改成功！'}
META_ERROR = {'status': 404, 'msg': '修改失败！该用户不存在！'}


@app.route('/user/edit', methods=['PUT'])
@handle_response
@verify_edit_user_request
def user_edit():
    body = request.json
    username = body['username']
    body.pop('username')

    if 'password' in body:
        body['password'] = encrypt_password(body['password'])

    user_mongodb_dao = UserMongoDBDao(user_collection)
    user = user_mongodb_dao.get_user(username)

    if not user:
        return {'meta': META_ERROR}

    user_mongodb_dao.edit_user(username, body)
    return {'meta': META_SUCCESS}
