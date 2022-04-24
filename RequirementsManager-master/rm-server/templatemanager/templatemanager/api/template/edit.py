from flask import request

from templatemanager.app import app
from templatemanager.dao.template import (
    Template, TemplateMongoDBDao
)
from templatemanager.mongodb import template_collection
from templatemanager.utils.handle_api import handle_response

import time

META_SUCCESS = {'status': 200, 'msg': '修改成功！'}
META_ERROR = {'status': 404, 'msg': '修改失败！该模板不存在！'}


@app.route('/template/edit', methods=['PUT'])
@handle_response
# @verify_system_role
def template_edit():
    body = request.json

    new_template = Template(**body)
    new_template.last_time = time.asctime(time.localtime())
    new_template.outline = list(filter(lambda x: len(x) > 0, new_template.outline))

    template_name = new_template.template_name
    template_mongodb_dao = TemplateMongoDBDao(template_collection)

    # check if template not exists
    template = template_mongodb_dao.get_template(template_name)
    if not template:
        return {'meta': META_ERROR}

    template_mongodb_dao.edit_template(template_name, new_template.jsonify())
    return {'meta': META_SUCCESS}

# from usermanager.app import app
# from usermanager.dao.user import UserMongoDBDao
# from usermanager.mongodb import user_collection
# from usermanager.utils.handle_api import (
#     verify_edit_user_request, handle_response
# )
# from usermanager.utils.password import encrypt_password
#
# META_SUCCESS = {'status': 200, 'msg': '修改成功！'}
# META_ERROR = {'status': 404, 'msg': '修改失败！该用户不存在！'}
#
#
# @app.route('/user/edit', methods=['PUT'])
# @handle_response
# @verify_edit_user_request
# def user_edit():
#     body = request.json
#     username = body['username']
#     body.pop('username')
#
#     if 'password' in body:
#         body['password'] = encrypt_password(body['password'])
#
#     user_mongodb_dao = UserMongoDBDao(user_collection)
#     user = user_mongodb_dao.get_user(username)
#
#     if not user:
#         return {'meta': META_ERROR}
#
#     user_mongodb_dao.edit_user(username, body)
#     return {'meta': META_SUCCESS}
