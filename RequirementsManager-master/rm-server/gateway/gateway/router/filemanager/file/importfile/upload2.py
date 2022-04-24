from flask import request

from gateway.app import app
from gateway.http_client import filemanager_http_client
from gateway.utils.handle_api import (
    get_client_username,handle_request_response
)


@app.route('/file/importfile/upload2',methods=['POST'])
@handle_request_response
@get_client_username
def file_importfile_upload2(client_username: str):
    supload_file = request.files['strufile']
    rupload_file = request.files['relafile']
    fileid=request.form['fileid']
    files = {'strufile': (supload_file.filename, supload_file.read()),
             'relafile': (rupload_file.filename, rupload_file.read()),}
    status_code, resp_body = filemanager_http_client.post(
        'file/importfile/upload2', client_username, files=files, params={'fileid':fileid}
    )
    return status_code, resp_body