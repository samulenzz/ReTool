import os

from flask import request
from templatemanager.app import app
from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.uuid import generate_uuid

META_SUCCESS = {'status': 200, 'msg': '删除成功！'}
META_ERROR_NO_DOCUMENT = {'status': 404, 'msg': '删除失败，文档不存在！'}


@app.route('/document/delete', methods=['DELETE'])
@handle_response
def document_delete():
    body = request.json

    document_id = body['document_id']

    document_mongodb_dao = DocumentMongoDBDao(document_collection)

    if not document_mongodb_dao.get_document(document_id):
        return {'meta': META_ERROR_NO_DOCUMENT}

    document_mongodb_dao.delete_document(document_id)
    return {'meta': META_SUCCESS}
