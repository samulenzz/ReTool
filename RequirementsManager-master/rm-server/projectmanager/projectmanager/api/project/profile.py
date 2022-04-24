from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_collection
)
from projectmanager.dao.project import (
    ProjectMongoDBDao
)
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}


@app.route('/project/profile', methods=['GET'])
@verify_request(['project', 'access'], access='project_profile')
@handle_response
def project_profile():
    project_id = request.args.get('project_id')

    project_dao = ProjectMongoDBDao(project_collection)

    # 获取项目信息
    project = project_dao.get_project(project_id)
    return {
        'data': project.jsonify(),
        'meta': META_SUCCESS
    }
