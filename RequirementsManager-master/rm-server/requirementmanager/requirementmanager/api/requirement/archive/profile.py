from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    archive_requirement_collection
)
from requirementmanager.dao.archive import (
    ArchiveRequirementMongoDBDao
)
from requirementmanager.utils.handle_api import handle_response
from requirementmanager.utils.verify import verify_project_user_role_access
from requirementmanager.utils.client_username import get_client_username


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}
META_ERROR_NO_REQUIREMENT = {'status': 404, 'msg': '获取失败！需求条目不存在！'}
META_ERROR_NO_ACCESS = {'status': 403, 'msg': '获取失败！没有操作权限！'}


@app.route('/requirement/archive/profile', methods=['GET'])
@handle_response
def requirement_archive_profile():
    client_username = get_client_username()
    requirement_id = request.args.get('requirement_id')
    version = request.args.get('version')

    archive_requirement_dao = ArchiveRequirementMongoDBDao(
        archive_requirement_collection
    )

    # 获取需求，需求是否存在
    archive_requirement = archive_requirement_dao.get(requirement_id, version)
    if not archive_requirement:
        return {
            'meta': META_ERROR_NO_REQUIREMENT
        }

    # 在内部而不是用装饰器判断是否有权限，因为需要根据requirement获取project_id
    is_access = verify_project_user_role_access(
        archive_requirement.project_id, client_username, 'requirement_archive_profile'
    )
    if not is_access:
        return {
            'meta': META_ERROR_NO_ACCESS
        }

    return {
        'meta': META_SUCCESS,
        'data': archive_requirement.jsonify()
    }
