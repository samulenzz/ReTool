from flask import request

from gateway.app import app
from gateway.http_client import usermanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/user/list_all', methods=['GET'])
@handle_request_response
@get_client_username
def user_list_all(client_username: str):
    status_code, resp_body = usermanager_http_client.get(
        'user/list_all', client_username
    )
    return status_code, resp_body
