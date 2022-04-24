from flask import request
from filemanager.app import app
from filemanager.utils.handle_api import handle_response
from filemanager.dao.file import FileMongoDBDao,File
from filemanager.mongodb import file_collection

META_SUCCESS = {'status': 200, 'msg': '创建成功！'}

@app.route('/file/create',methods=['POST'])
@handle_response
def file_create():
    body = request.json
    file_dao=FileMongoDBDao(file_collection)

    file=File(**body)
    file_dao.create_file(file)
    file_id=file._id

    return {
        'meta':META_SUCCESS,
        'data':file_id
    }
