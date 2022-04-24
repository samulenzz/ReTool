import json
from typing import Callable
from functools import wraps
from urllib.parse import unquote

from flask import request, Response

from usermanager.mongodb import user_collection
from usermanager.dao.user import (
    UserMongoDBDao
)
from usermanager.dao.user import SYSTEM_ROLE_SYSTEM_MANAGER


META_NO_ACCESS = {'status': 403, 'msg': '没有操作权限！'}


def verify_system_role(func: Callable):
    @wraps(func)
    def _func():
        client_username = request.headers.get('Client-Username')
        # 对Headers中的中文进行解码
        client_username = unquote(client_username)
        user_mongodb_dao = UserMongoDBDao(user_collection)
        client_user = user_mongodb_dao.get_user(client_username)

        if not client_user or client_user.system_role != SYSTEM_ROLE_SYSTEM_MANAGER:
            return {'meta': META_NO_ACCESS}
        return func()

    return _func


def verify_edit_user_request(func: Callable):
    @wraps(func)
    def _func():
        client_username = request.headers.get('Client-Username')
        # 对Headers中的中文进行解码
        client_username = unquote(client_username)
        user_mongodb_dao = UserMongoDBDao(user_collection)
        client_user = user_mongodb_dao.get_user(client_username)

        if not client_user:
            return {'meta': META_NO_ACCESS}
        # 如果用户是管理员，则放行
        if client_user.system_role == SYSTEM_ROLE_SYSTEM_MANAGER:
            return func()
        # 或者用户名和body中的用户名相等，且没有system_role字段则放行
        if client_user.username == request.json['username'] and \
            'system_role' not in request.json:
            return func()

        return {'meta': META_NO_ACCESS}

    return _func


def handle_response(func: Callable):
    @wraps(func)
    def _func():
        resp = func()
        return Response(json.dumps(resp), mimetype='application/json')

    return _func
