import json
from typing import Callable, List
from functools import wraps

from flask import request, Response

from requirementmanager.utils.verify import verify_project_user_role_access
from requirementmanager.utils.client_username import get_client_username


META_ERROR_NO_ACCESS = {'status': 403, 'msg': '没有操作权限！'}


def handle_response(func: Callable):
    @wraps(func)
    def _func():
        resp = func()
        # 对结果进行排序
        r=Response(json.dumps(resp), mimetype='application/json')
        return r

    return _func


def verify_request(verify_type: List[str], **kwargs):
    def _wrapper(func: Callable):
        @wraps(func)
        def _func():
            client_username = get_client_username()
            for _type in verify_type:
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
            return func()
        return _func
    return _wrapper
