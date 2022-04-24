from flask import request

from gateway.app import app
from gateway.http_client import projectmanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/project/edit', methods=['PUT'])
@handle_request_response
@get_client_username
def project_edit(client_username: str):
    body = request.json
    status_code, resp_body = projectmanager_http_client.put(
        'project/edit', client_username, json=body
    )
    return status_code, resp_body
