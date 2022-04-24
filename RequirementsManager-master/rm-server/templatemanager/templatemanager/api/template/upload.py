import os

from flask import request
from templatemanager.app import app
from templatemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '上传成功！'}
META_ERROR_BAD_FILE = {'status': 400, 'msg': '上传失败，文件格式错误！'}

UPLOAD_FILE_DIRNAME = 'uploads'
os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)


@app.route('/template/upload', methods=['POST'])
@handle_response
def template_upload():
    upload_file = request.files['file']
    if not upload_file.filename.endswith('.docx'):
        return {
            'meta': META_ERROR_BAD_FILE
        }

    # 提取文件名(不包含扩展名)作为模板名
    filename = os.path.splitext(upload_file.filename)[0]
    filepath = os.path.join(UPLOAD_FILE_DIRNAME, f'{filename}.docx')
    upload_file.save(filepath)
    return {
        'meta': META_SUCCESS,
        'data': {
            'token': filename
        }
    }
