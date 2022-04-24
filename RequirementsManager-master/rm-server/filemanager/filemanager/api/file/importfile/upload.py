import os
from flask import request

from filemanager.app import app
from filemanager.utils.handle_api import handle_response
from filemanager.utils.uuid import generate_uuid

META_SUCCESS = {'status': 200, 'msg': '上传成功！'}
META_ERROR_BAD_FILE = {'status': 400, 'msg': '上传失败，文件格式错误！'}

UPLOAD_FILE_DIRNAME = r'zduploads\RE'
os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)

@app.route('/file/importfile/upload',methods=['POST'])
@handle_response
def file_importfile_upload():
    upload_file = request.files['file']
    fileid=request.args.get('fileid')
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