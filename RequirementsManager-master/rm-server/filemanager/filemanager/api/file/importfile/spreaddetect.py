import os

from flask import request
from filemanager.app import app
from filemanager.utils.handle_api import handle_response
from filemanager.api.file.spreaddetect.getSpreadData import getSpreadData


META_SUCCESS = {'status': 200, 'msg': '分析成功！'}
META_ERROR_NO_FILE = {'status': 404, 'msg': '分析失败，文件不存在！'}

STRU_FILE_DIRNAME = r'zduploads\stru'
RELA_FILE_DIRNAME = r'zduploads\rela'
RES1_FILE_DIRNAME = r'SpreadTXT'
os.makedirs(STRU_FILE_DIRNAME, exist_ok=True)
os.makedirs(RELA_FILE_DIRNAME, exist_ok=True)
os.makedirs(RES1_FILE_DIRNAME, exist_ok=True)

@app.route('/file/importfile/spreaddetect',methods=['POST'])
@handle_response
def file_importfile_spreaddetect():
    body = request.json
    # filetoken = body['token']
    fileid=body['fileId'] #文档的标号
    filename = f'{fileid}.json'
    sfilepath = os.path.join(STRU_FILE_DIRNAME, filename)
    rfilepath = os.path.join(RELA_FILE_DIRNAME, filename)

    # 检测文件是否存在
    if not (os.path.exists(sfilepath) and os.path.exists(rfilepath)):
        return {
            'meta': META_ERROR_NO_FILE
        }

    # 进行模糊语句检测
    resp_data=getSpreadData(sfilepath,rfilepath)

    # 保存检测结果，文件名与文档名保持一致以方便getscope
    restxt=f'{fileid}.txt'
    restxtpath=os.path.join(RES1_FILE_DIRNAME, restxt)
    fout=open(restxtpath,"w",encoding='UTF-8')
    fout.write(resp_data)

    return {
        'meta': META_SUCCESS,
        'data': resp_data
    }