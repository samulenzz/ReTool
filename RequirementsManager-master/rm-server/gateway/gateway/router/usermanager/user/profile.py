from flask import request

from gateway.app import app
from gateway.http_client import usermanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/user/profile', methods=['GET'])
@handle_request_response
@get_client_username
def user_profile(client_username: str):
    args = request.args.to_dict()
    status_code, resp_body = usermanager_http_client.get(
        'user/profile', client_username, params=args
    )
    return status_code, resp_body
