from flask import request

from projectmanager.app import app
from projectmanager.utils.handle_api import handle_response
from projectmanager.utils.verify import (
    verify_project_exist, verify_project_user_role_access
)


META_SUCCESS = {'status': 200, 'msg': '权限检查成功！'}


@app.route('/project/user/role/verify', methods=['POST'])
@handle_response
def project_user_role_verify():
    body = request.json

    if not verify_project_exist(body['project_id']):
        return {
            'meta': META_SUCCESS,
            'data': False
        }

    is_access = verify_project_user_role_access(
        body['project_id'],
        body['username'],
        body['access']
    )
    return {
        'meta': META_SUCCESS,
        'data': is_access,
    }
