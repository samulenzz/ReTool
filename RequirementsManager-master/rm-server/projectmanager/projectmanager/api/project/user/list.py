from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_userlist_collection
)
from projectmanager.dao.project_userlist import ProjectUserListMongoDBDao
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}


@app.route('/project/user/list', methods=['GET'])
@verify_request(['project', 'access'], access='project_user_list')
@handle_response
def project_user_list():
    project_id = request.args.get("project_id")

    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )

    # 获取项目内用户列表
    project_users = project_userlist_dao.get_all_users(project_id)
    resp = [user.jsonify() for user in project_users]
    return {
        'data': resp,
        'meta': META_SUCCESS
    }
