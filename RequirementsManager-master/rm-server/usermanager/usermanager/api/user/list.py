from usermanager.app import app
from usermanager.dao.user_list import (
    UserListMongoDBDao
)
from usermanager.mongodb import user_collection
from usermanager.utils.handle_api import handle_response


META_SUCCESS = {'status': 200, 'msg': '成功！'}


@app.route('/user/list', methods=['GET'])
@handle_response
def user_list():
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
