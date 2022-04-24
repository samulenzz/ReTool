from flask import request
import os

from filemanager.app import app
from filemanager.mongodb import file_collection
from filemanager.dao.file import FileMongoDBDao
from filemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '获取成功！'}
META_ERROR_NO_FILE = {'status': 404, 'msg': '无对应检测结果！'}

RES1_FILE_DIRNAME = r'UncertainTXT'

@app.route('/file/getscope',methods=['GET'])
@handle_response
def file_getscope():
    file_id=request.args.get('file_id')

    restxt = f'{file_id}.txt'
    restxtpath = os.path.join(RES1_FILE_DIRNAME, restxt)

    if not os.path.exists(restxtpath):
        return {
            'meta': META_ERROR_NO_FILE
        }

    fin = open(restxtpath, "r", encoding='UTF-8')
    resp_data=""
    for line in fin.readlines():
        line=line.strip()
        resp_data+=line

    return {
        'meta': META_SUCCESS,
        'data': resp_data
    }