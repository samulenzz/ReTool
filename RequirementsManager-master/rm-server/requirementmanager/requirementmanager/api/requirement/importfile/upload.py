import os

from flask import request

from requirementmanager.app import app
from requirementmanager.utils.handle_api import handle_response
from requirementmanager.utils.uuid import generate_uuid


META_SUCCESS = {'status': 200, 'msg': '上传成功！'}
META_ERROR_BAD_FILE = {'status': 400, 'msg': '上传失败，文件格式错误！'}

UPLOAD_FILE_DIRNAME = 'uploads'
os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)


@app.route('/requirement/importfile/upload', methods=['POST'])
@handle_response
def requirement_importfile_upload():
    upload_file = request.files['file']
    if (not upload_file.filename.endswith('.doc')) and \
       (not upload_file.filename.endswith('.docx')):
        return {
           'meta': META_ERROR_BAD_FILE
        }

    # 生成随机文件名，保存
    filename = generate_uuid()
    filepath = os.path.join(UPLOAD_FILE_DIRNAME, f'{filename}.docx')
    upload_file.save(filepath)

    return {
        'meta': META_SUCCESS,
        'data': {
            'token': filename
        }
    }
