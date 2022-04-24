from flask import request

from gateway.app import app
from gateway.http_client import projectmanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/project/user/list', methods=['GET'])
@handle_request_response
@get_client_username
def project_user_list(client_username: str):
    args = request.args.to_dict()
    status_code, resp_body = projectmanager_http_client.get(
        'project/user/list', client_username, params=args
    )
    return status_code, resp_body
