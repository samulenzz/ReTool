from flask import request

from gateway.app import app
from gateway.http_client import filemanager_http_client
from gateway.utils.handle_api import (
    get_client_username,handle_request_response
)


@app.route('/file/importfile/upload',methods=['POST'])
@handle_request_response
@get_client_username
def file_importfile_upload(client_username: str):
    upload_file = request.files['file']
    fileid=request.form['fileid']
    files = {'file': (upload_file.filename, upload_file.read())}
    status_code, resp_body = filemanager_http_client.post(
        'file/importfile/upload', client_username, files=files, params={'fileid':fileid}
    )
    return status_code, resp_body