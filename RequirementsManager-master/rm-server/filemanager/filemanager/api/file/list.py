from flask import request

from filemanager.app import app
from filemanager.mongodb import file_collection
from filemanager.dao.file import  FileMongoDBDao
from filemanager.dao.file_list import FileListMongoDBDao
from filemanager.mongodb import file_collection
from filemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '获取成功！'}

@app.route('/file/list',methods=['GET'])
@handle_response
def file_list():
    file_list_dao=FileListMongoDBDao(file_collection)

    files=file_list_dao.get_all_files()

    resp=[file.jsonify() for file in files]

    return {
        'data':resp,
        'meta': META_SUCCESS
    }