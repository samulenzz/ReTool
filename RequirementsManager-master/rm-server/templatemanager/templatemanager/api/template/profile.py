# from flask import request
#
# from usermanager.app import app
# from usermanager.dao.user import UserMongoDBDao
# from usermanager.mongodb import user_collection
# from usermanager.utils.handle_api import handle_response
#
#
# META_SUCCESS = {'status': 200, 'msg': '成功！'}
# META_ERROR = {'status': 404, 'msg': '失败！该用户不存在！'}
#
#
# @app.route('/user/profile', methods=['GET'])
# @handle_response
# def user_profile():
#     username = request.args.get("username")
#     user_mongodb_dao = UserMongoDBDao(user_collection)
#
#     user = user_mongodb_dao.get_user(username)
#     if not user:
#         return {'meta': META_ERROR}
#
#     # Remove password attribute
#     data = user.jsonify()
#     data.pop('password')
#     return {'data': data, 'meta': META_SUCCESS}
