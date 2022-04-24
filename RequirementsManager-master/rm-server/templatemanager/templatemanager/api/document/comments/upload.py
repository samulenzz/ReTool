import os

from flask import request
from templatemanager.app import app

from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.config import UPLOAD_FILE_DIRNAME
from templatemanager.utils.handle_api import handle_response

META_SUCCESS = {'status': 200, 'msg': '创建成功！'}
META_ERROR_BAD_FILE = {'status': 400, 'msg': '上传失败，文件格式错误！'}
META_ERROR = {'status': 405, 'msg': '失败，未找到所属文档！'}


@app.route('/document/comments/upload', methods=['POST'])
@handle_response
def comments_upload():
    # body = request.json
    document_id = request.form['document_id']
    upload_file = request.files['file']
    if not upload_file.filename.endswith('.csv'):
        return {'meta': META_ERROR_BAD_FILE}

    filename = os.path.splitext(upload_file.filename)[0]

    os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)

    filepath = os.path.join(UPLOAD_FILE_DIRNAME, f'{filename}.csv')
    upload_file.save(filepath)

    document_dao = DocumentMongoDBDao(document_collection)

    document = document_dao.get_document(document_id)

    if document is None:
        return {'meta': META_ERROR}

    document.comments_file_list.append(filename)

    document_dao.edit_document(document_id, document.jsonify())

    return {'meta': META_SUCCESS}
