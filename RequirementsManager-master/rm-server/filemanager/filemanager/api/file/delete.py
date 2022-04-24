from flask import request

from filemanager.app import app
from filemanager.mongodb import file_collection
from filemanager.dao.file import FileMongoDBDao
from filemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '删除成功！'}

@app.route('/file/delete',methods=['DELETE'])
@handle_response
def file_delete():
    body = request.json
    file_id=body['file_id']

    file_dao=FileMongoDBDao(file_collection)

    file_dao.delete_file(file_id)

    return {
        'meta': META_SUCCESS
    }