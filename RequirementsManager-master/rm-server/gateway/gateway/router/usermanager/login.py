from flask import request

from gateway.app import app
from gateway.http_client import usermanager_http_client
from gateway.authtoken import (
    Token, TokenStorage, token_storage
)
from gateway.utils.handle_api import handle_request_response


@app.route('/login', methods=['POST'])
@handle_request_response
def login():
    body = request.json
    username = body['username']
    status_code, resp_body = usermanager_http_client.post(
        endpoint='login', json=body
    )
    if status_code == 200 and resp_body['meta']['status'] == 200:
        token_value = resp_body['data']['token']
        token = Token(username, token_value)
        token_storage.add_token(token)

    return status_code, resp_body
