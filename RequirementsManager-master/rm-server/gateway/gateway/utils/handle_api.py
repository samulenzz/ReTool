import json
from typing import Callable
from functools import wraps

from flask import request, Response

from gateway.authtoken import token_storage


def handle_request_response(func: Callable):

    @wraps(func)
    def _func(*args, **kwargs):
        print(request.headers)
        print(request.data)
        status_code = None
        try:
            status_code, resp_body = func(*args, **kwargs)
        except Exception as e:
            print(e)
            resp_body = {'meta': {'status': 500, 'msg': 'Internal Server Error'}}

        if status_code and status_code != 200:
            resp_body = {'meta': {'status': 500, 'msg': 'Internal Server Error'}}
        print(resp_body)
        return Response(json.dumps(resp_body), mimetype='application/json')

    return _func


def get_client_username(func: Callable):

    @wraps(func)
    def _func(*args, **kwargs):
        token_value = request.headers.get('Authorization', None)
        if not token_value:
            return 200, {'meta': {'status': 401, 'msg': '身份认证失败！'}}
        client_username = token_storage.get_username(token_value)
        if not client_username:
            return 200, {'meta': {'status': 401, 'msg': '身份认证失败！'}}
        return func(*args, client_username=client_username, **kwargs) 

    return _func
