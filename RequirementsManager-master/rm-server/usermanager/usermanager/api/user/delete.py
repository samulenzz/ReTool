from flask import request

from usermanager.app import app
from usermanager.dao.user import UserMongoDBDao
from usermanager.mongodb import user_collection
from usermanager.utils.handle_api import verify_system_role, handle_response


META_SUCCESS = {'status': 200, 'msg': '删除成功！'}
META_ERROR = {'status': 404, 'msg': '删除失败！该用户不存在！'}


@app.route('/user/delete', methods=['DELETE'])
@handle_response
@verify_system_role
def user_delete():
    body = request.json
    username = body['username']
    user_mongodb_dao = UserMongoDBDao(user_collection)

    if not user_mongodb_dao.get_user(username):
        return {'meta': META_ERROR}

    user_mongodb_dao.delete_user(username)
    return {'meta': META_SUCCESS}
