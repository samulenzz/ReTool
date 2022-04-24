from flask import request

from gateway.app import app
from gateway.http_client import requirementmanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/requirement/importfile/upload', methods=['POST'])
@handle_request_response
@get_client_username
def requirement_importfile_upload(client_username: str):
    upload_file = request.files['file']
    files = {'file': (upload_file.filename, upload_file.read())}

    status_code, resp_body = requirementmanager_http_client.post(
        'requirement/importfile/upload', client_username, files=files
    )
    return status_code, resp_body
