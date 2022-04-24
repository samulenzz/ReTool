from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_collection, project_userlist_collection
)
from projectmanager.dao.project_list import ProjectListMongoDBDao
from projectmanager.dao.project_userlist import ProjectUserListMongoDBDao
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}


@app.route('/project/list', methods=['GET'])
@verify_request(['username'])
@handle_response
def project_list():
    username = request.args.get("username")

    project_list_dao = ProjectListMongoDBDao(project_collection)
    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )

    projects_ids = project_userlist_dao.get_projects_by_user(username)
    projects = project_list_dao.get_projects_by_ids(projects_ids)

    resp = [project.jsonify() for project in projects]

    return {
        'data': resp,
        'meta': META_SUCCESS
    }
