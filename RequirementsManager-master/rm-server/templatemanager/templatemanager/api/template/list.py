from templatemanager.app import app
from templatemanager.dao.template_list import (
    TemplateListMongoDBDao
)
from templatemanager.mongodb import template_collection
from templatemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '成功！'}


@app.route('/template/list', methods=['GET'])
@handle_response
def template_list():
    template_list_mongodb_dao = TemplateListMongoDBDao(template_collection)
    templates = template_list_mongodb_dao.get_all_templates()
    data = []
    for template in templates:
        # tmp_template = template.jsonify()
        data.append(template.jsonify())
    return {
        'data': data,
        'meta': META_SUCCESS,
    }

# from usermanager.app import app
# from usermanager.dao.user_list import (
#     UserListMongoDBDao
# )
# from usermanager.mongodb import user_collection
# from usermanager.utils.handle_api import handle_response
#
#
# META_SUCCESS = {'status': 200, 'msg': '成功！'}
#
#
# @app.route('/user/list', methods=['GET'])
# @handle_response
# def user_list():
#     user_list_mongodb_dao = UserListMongoDBDao(user_collection)
#     users = user_list_mongodb_dao.get_all_users()
#     data = []
#     for user in users:
#         tmp_user = user.jsonify()
#         tmp_user.pop('password')
#         data.append(tmp_user)
#     return {
#         'data': data,
#         'meta': META_SUCCESS
#     }
