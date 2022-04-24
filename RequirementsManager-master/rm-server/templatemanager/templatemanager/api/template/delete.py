from flask import request

from templatemanager.app import app
from templatemanager.dao.template import (
    Template, TemplateMongoDBDao
)
from templatemanager.mongodb import template_collection
from templatemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '删除成功！'}
META_ERROR = {'status': 404, 'msg': '删除失败！该模板不存在！'}


@app.route('/template/delete', methods=['DELETE'])
@handle_response
# @verify_system_role
def template_delete():
    body = request.json
    template_mongodb_dao = TemplateMongoDBDao(template_collection)
    template_name = body['template_name']
    # check if template not exists
    if not template_mongodb_dao.get_template(template_name):
        return {'meta': META_ERROR}
    template_mongodb_dao.delete_template(template_name)
    return {"meta": META_SUCCESS}

# from usermanager.app import app
# from usermanager.dao.user import UserMongoDBDao
# from usermanager.mongodb import user_collection
# from usermanager.utils.handle_api import verify_system_role, handle_response
#
#
# META_SUCCESS = {'status': 200, 'msg': '删除成功！'}
# META_ERROR = {'status': 404, 'msg': '删除失败！该用户不存在！'}
#
#
# @app.route('/user/delete', methods=['DELETE'])
# @handle_response
# @verify_system_role
# def template_delete():
#     body = request.json
#     username = body['username']
#     user_mongodb_dao = UserMongoDBDao(user_collection)
#
#     if not user_mongodb_dao.get_user(username):
#         return {'meta': META_ERROR}
#
#     user_mongodb_dao.delete_user(username)
#     return {'meta': META_SUCCESS}
