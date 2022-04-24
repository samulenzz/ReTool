import os
from flask import request

from filemanager.app import app
from filemanager.utils.handle_api import handle_response
from filemanager.utils.uuid import generate_uuid

META_SUCCESS = {'status': 200, 'msg': '上传成功！'}
META_ERROR_BAD_FILE = {'status': 400, 'msg': '上传失败，文件格式错误！'}

STRU_FILE_DIRNAME = r'zduploads\stru'
RELA_FILE_DIRNAME = r'zduploads\rela'
os.makedirs(STRU_FILE_DIRNAME, exist_ok=True)
os.makedirs(RELA_FILE_DIRNAME, exist_ok=True)

@app.route('/file/importfile/upload2',methods=['POST'])
@handle_response
def file_importfile_upload2():
    stru_file=request.files['strufile']
    rela_file=request.files['relafile']
    fileid=request.args.get('fileid')
    if (not stru_file.filename.endswith('.json')) or \
            (not rela_file.filename.endswith('.json')):
        return {
            'meta': META_ERROR_BAD_FILE
        }

    # 生成随机文件名，保存
    sfilepath = os.path.join(STRU_FILE_DIRNAME, f'{fileid}.json')
    rfilepath = os.path.join(RELA_FILE_DIRNAME, f'{fileid}.json')
    stru_file.save(sfilepath)
    rela_file.save(rfilepath)

    return {
        'meta': META_SUCCESS,
        'data': {
            'token': fileid
        }
    }