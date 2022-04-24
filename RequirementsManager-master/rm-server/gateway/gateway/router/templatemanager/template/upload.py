from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/template/upload', methods=['POST'])
@handle_request_response
@get_client_username
def template_upload(client_username: str):
    upload_file = request.files['file']
    files = {'file': (upload_file.filename, upload_file.read())}
    status_code, resp_body = templatemanager_http_client.post(
        'template/upload', client_username, files=files
    )
    return status_code, resp_body
