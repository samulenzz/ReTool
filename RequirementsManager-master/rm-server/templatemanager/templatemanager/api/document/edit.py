import os

from flask import request
from templatemanager.app import app
from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.uuid import generate_uuid

from time import asctime, localtime

META_SUCCESS = {'status': 200, 'msg': '修改成功！'}
META_ERROR_NO_DOCUMENT = {'status': 404, 'msg': '修改失败，该文档不存在！'}


@app.route('/document/edit', methods=['POST'])
@handle_response
def document_edit():
    body = request.json
    document_dict = body['document']
    document = Document(**document_dict)
    # update the time
    document.last_time = asctime(localtime())

    document_id = document._id

    document_mongodb_dao = DocumentMongoDBDao(document_collection)

    if not document_mongodb_dao.get_document(document_id):
        return {'meta': META_ERROR_NO_DOCUMENT}

    document_mongodb_dao.edit_document(document_id, document.jsonify())
    return {'meta': META_SUCCESS}
