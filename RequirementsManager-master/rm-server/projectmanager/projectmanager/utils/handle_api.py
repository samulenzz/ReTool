import json
from typing import Callable, List
from functools import wraps

from flask import request, Response

from projectmanager.utils.verify import (
    verify_project_exist, verify_project_user_role_access
)
from projectmanager.utils.client_username import get_client_username


META_ERROR_NO_PROJECT = {'status': 404, 'msg': '失败！项目不存在！'}
META_ERROR_NO_ACCESS = {'status': 403, 'msg': '失败！没有权限操作！'}


def handle_response(func: Callable):
    @wraps(func)
    def _func():
        resp = func()
        # 对结果进行排序
        return Response(json.dumps(resp), mimetype='application/json')

    return _func


def verify_request(verify_type: List[str], **kwargs):
    def _wrapper(func: Callable):
        @wraps(func)
        def _func():
            client_username = get_client_username()
            for _type in verify_type:
                # 检验项目id是否存在
                if _type == 'project':
                    if request.method == 'GET':
                        project_id = request.args.get("project_id")
                    else:
                        project_id = request.json['project_id']
                    if not verify_project_exist(project_id):
                        return {
                            'meta': META_ERROR_NO_PROJECT
                        }
                # 检验有无权限
                if _type == 'access':
                    if request.method == 'GET':
                        project_id = request.args.get("project_id")
                    else:
                        project_id = request.json['project_id']
                    is_access = verify_project_user_role_access(
                        project_id, client_username, kwargs['access']
                    )
                    if not is_access:
                        return {
                            'meta': META_ERROR_NO_ACCESS
                        }
                # 检验用户名和实际操作用户名是否一致
                if _type == 'username':
                    username = request.args.get("username")
                    if client_username != username:
                        return {
                            'meta': META_ERROR_NO_ACCESS
                        }
            return func()
        return _func
    return _wrapper
