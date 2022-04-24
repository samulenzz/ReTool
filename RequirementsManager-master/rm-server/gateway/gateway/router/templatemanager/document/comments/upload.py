from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/document/comments/upload', methods=['POST'])
@handle_request_response
@get_client_username
def comments_upload(client_username: str):
    upload_file = request.files['file']
    document_id = request.form['document_id']
    files = {
        'file': (upload_file.filename, upload_file.read()),
        'document_id': (None, document_id)
    }
    status_code, resp_body = templatemanager_http_client.post(
        'document/comments/upload', client_username, files=files
    )
    return status_code, resp_body
