import os

from flask import request
from filemanager.app import app
from filemanager.utils.handle_api import handle_response
from filemanager.api.file.uncertaindetect.getUncertainData import getUncertainData

from filemanager.dao.file import FileMongoDBDao
from filemanager.mongodb import file_collection

META_SUCCESS = {'status': 200, 'msg': '检测成功！'}
META_ERROR_NO_FILE = {'status': 404, 'msg': '检测失败，文件不存在！'}

UPLOAD_FILE_DIRNAME = r'zduploads\RE'
RES1_FILE_DIRNAME = r'UncertainTXT'
os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)

@app.route('/file/importfile/uncertaindetect',methods=['POST'])
@handle_response
def file_importfile_uncertaindetect():
    body = request.json
    # filetoken = body['token']
    fileid=body['fileId'] #文档的标号
    filetoken=body['uploadFileToken'] #之前上传的doc的标号
    filename = f'{filetoken}.docx'
    filepath = os.path.join(UPLOAD_FILE_DIRNAME, filename)

    # 检测文件是否存在
    if not os.path.exists(filepath):
        return {
            'meta': META_ERROR_NO_FILE
        }

    # 进行模糊语句检测
    resp_data=getUncertainData(filepath)

    # 保存检测结果，文件名与文档名保持一致以方便getscope
    restxt=f'{fileid}.txt'
    restxtpath=os.path.join(RES1_FILE_DIRNAME, restxt)
    fout=open(restxtpath,"w",encoding='UTF-8')
    fout.write(resp_data)

    return {
        'meta': META_SUCCESS,
        'data': resp_data
    }