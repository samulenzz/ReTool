from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/document/list', methods=['GET'])
@handle_request_response
@get_client_username
def document_list(client_username: str):
    status_code, resp_body = templatemanager_http_client.get(
        'document/list', client_username
    )
    return status_code, resp_body
