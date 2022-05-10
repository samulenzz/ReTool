from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_collection, project_userlist_collection, baseline_collection
)
from projectmanager.dao.project import (
    ProjectMongoDBDao, Project
)
from projectmanager.dao.project_userlist import (
    ProjectUserListMongoDBDao, ProjectUser
)
from projectmanager.dao.baseline import (
    BaselineMongoDBDao
)
from projectmanager.utils.handle_api import handle_response


META_SUCCESS = {'status': 200, 'msg': '创建成功！'}


@app.route('/project/create', methods=['POST'])
@handle_response
def project_create():
    body = request.json
    # 将users分离
    users = body.pop('users')
    users = [ProjectUser(**user) for user in users]

    project_dao = ProjectMongoDBDao(project_collection)
    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )
    baseline_dao = BaselineMongoDBDao(baseline_collection)

    project = Project(**body)
    # 创建project
    project_dao.create_project(project)
    # 创建project_userlist
    project_userlist_dao.create(project._id)
    # 向project_userlist添加用户
    project_userlist_dao.edit_users(project._id, users)
    # 初始化基线
    baseline_dao.create(project._id)
    return {
        'project_id': project._id,
        'meta': META_SUCCESS
    }
