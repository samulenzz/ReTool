from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/template/edit', methods=['PUT'])
@handle_request_response
@get_client_username
def template_edit(client_username: str):
    body = request.json
    status_code, resp_body = templatemanager_http_client.put(
        'template/edit', client_username, json=body
    )
    return status_code, resp_body
