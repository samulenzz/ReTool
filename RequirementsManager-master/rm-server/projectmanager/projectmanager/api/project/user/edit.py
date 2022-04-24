from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_userlist_collection
)
from projectmanager.dao.project_userlist import (
    ProjectUserListMongoDBDao, ProjectUser
)
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '修改成功！'}


@app.route('/project/user/edit', methods=['PUT'])
@verify_request(['project', 'access'], access='project_user_edit')
@handle_response
def project_user_edit():
    body = request.json
    project_id = body.pop('project_id')

    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )

    # 修改项目成员
    new_project_users = []
    for user_dict in body['users']:
        new_project_users.append(ProjectUser(**user_dict))
    project_userlist_dao.edit_users(project_id, new_project_users)
    return {
        'meta': META_SUCCESS
    }
