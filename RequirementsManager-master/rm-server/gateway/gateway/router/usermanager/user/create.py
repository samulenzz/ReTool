from flask import request

from gateway.app import app
from gateway.http_client import usermanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/user/create', methods=['POST'])
@handle_request_response
@get_client_username
def user_create(client_username: str):
    body = request.json
    status_code, resp_body = usermanager_http_client.post(
        'user/create', client_username, json=body
    )
    return status_code, resp_body
