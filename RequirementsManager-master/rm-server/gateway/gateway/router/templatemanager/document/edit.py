from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/document/edit', methods=['POST'])
@handle_request_response
@get_client_username
def document_edit(client_username: str):
    body = request.json
    status_code, resp_body = templatemanager_http_client.post(
        'document/edit', client_username, json=body
    )
    return status_code, resp_body
