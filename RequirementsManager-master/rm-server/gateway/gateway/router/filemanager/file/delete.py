from flask import request

from gateway.app import app
from gateway.http_client import filemanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)

@app.route('/file/delete', methods=['DELETE'])
@handle_request_response
@get_client_username
def file_delete(client_username: str):
    body = request.json
    status_code, resp_body = filemanager_http_client.delete(
        'file/delete', client_username, json=body
    )
    return status_code, resp_body