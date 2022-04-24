from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    project_collection, project_userlist_collection, baseline_collection
)
from projectmanager.dao.project import (
    ProjectMongoDBDao
)
from projectmanager.dao.project_userlist import (
    ProjectUserListMongoDBDao,
)
from projectmanager.dao.baseline import (
    BaselineMongoDBDao
)
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '删除成功！'}


@app.route('/project/delete', methods=['DELETE'])
@verify_request(['project', 'access'], access='project_delete')
@handle_response
def project_delete():
    body = request.json
    project_id = body['project_id']

    project_dao = ProjectMongoDBDao(project_collection)
    project_userlist_dao = ProjectUserListMongoDBDao(
        project_userlist_collection
    )
    baseline_dao = BaselineMongoDBDao(baseline_collection)

    # 删除项目
    project_dao.delete_project(project_id)
    project_userlist_dao.delete(project_id)
    baseline_dao.delete(project_id)
    return {
        'meta': META_SUCCESS
    }
