from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_collection
)
from projectmanager.dao.project import (
    ProjectMongoDBDao
)
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '修改成功！'}


@app.route('/project/edit', methods=['PUT'])
@verify_request(['project', 'access'], access='project_edit')
@handle_response
def project_edit():
    body = request.json
    project_id = body.pop('project_id')

    project_dao = ProjectMongoDBDao(project_collection)

    # 修改项目
    project_dao.edit_project(project_id, **body)
    return {
        'meta': META_SUCCESS
    }
