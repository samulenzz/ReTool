from datetime import datetime

from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    requirement_collection
)
from requirementmanager.dao.requirement import (
    RequirementMongoDBDao
)
from requirementmanager.utils.handle_api import handle_response
from requirementmanager.utils.verify import verify_project_user_role_access
from requirementmanager.utils.client_username import get_client_username


META_SUCCESS = {'status': 200, 'msg': '修改成功！'}
META_ERROR_NO_REQUIREMENT = {'status': 404, 'msg': '修改失败！需求条目不存在！'}
META_ERROR_NO_ACCESS = {'status': 403, 'msg': '修改失败！没有操作权限！'}


@app.route('/requirement/edit', methods=['PUT'])
@handle_response
def requirement_edit():
    body = request.json
    client_username = get_client_username()
    # 自动修改最后修改时间
    body['last_modify_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    requirement_id = body.pop('requirement_id')

    requirement_dao = RequirementMongoDBDao(requirement_collection)

    # 获取需求，需求是否存在
    requirement = requirement_dao.get(requirement_id)
    if not requirement:
        return {
            'meta': META_ERROR_NO_REQUIREMENT
        }

    # 在内部而不是用装饰器判断是否有权限，因为需要根据requirement获取project_id
    is_access = verify_project_user_role_access(
        requirement.project_id, client_username, 'requirement_edit'
    )
    if not is_access:
        return {
            'meta': META_ERROR_NO_ACCESS
        }

    # 修改需求
    requirement_dao.edit(requirement_id, **body)
    return {
        'meta': META_SUCCESS
    }
