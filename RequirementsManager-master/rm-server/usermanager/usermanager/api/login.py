from flask import request

from usermanager.app import app
from usermanager.dao.user import UserMongoDBDao
from usermanager.mongodb import user_collection
from usermanager.utils.authtoken import generate_token
from usermanager.utils.password import verify_password
from usermanager.utils.handle_api import handle_response


META_SUCCESS = {'status': 200, 'msg': '登录成功！'}
META_ERROR = {'status': 400, 'msg': '用户名或密码错误！'}


@app.route('/login', methods=['POST'])
@handle_response
def login():
    body = request.json
    username = body['username']
    password = body['password']
    # Check username and password
    user_mongodb_dao = UserMongoDBDao(user_collection)
    user = user_mongodb_dao.get_user(username)
    if not user:
        return {'meta': META_ERROR}
    if verify_password(password, user.password):
        # If correct, generate token
        token = generate_token()
        resp = {
            'data': {'token': token},
            'meta': META_SUCCESS
        }
    else:
        resp = {
            'meta': META_ERROR
        }
    return resp
