import os

from flask import request
from templatemanager.app import app
from templatemanager.dao.template import (
    Template, TemplateMongoDBDao
)
from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection, template_collection
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.uuid import generate_uuid

from time import asctime, localtime

META_SUCCESS = {'status': 200, 'msg': '创建成功！'}
META_ERROR_NO_TEMPLATE = {'status': 404, 'msg': '创建失败，对应模板不存在！'}


@app.route('/document/create', methods=['POST'])
@handle_response
def document_create():
    body = request.json

    template_name = body['template_name']
    document_name = body['document_name']
    introduction = body['introduction']

    template_mongodb_dao = TemplateMongoDBDao(template_collection)

    template = template_mongodb_dao.get_template(template_name)

    if not template:
        return {'meta': META_ERROR_NO_TEMPLATE}

    # document = Document(document_name, template_name,
    #                     introduction, template.outline)
    document = Document(_id=generate_uuid(),
                        document_name=document_name,
                        template_name=template_name,
                        introduction=introduction,
                        last_time=asctime(localtime()),
                        outline=[line for line in template.outline],
                        contents=["" for _ in template.outline],
                        comments_file_list=[])
    document_mongodb_dao = DocumentMongoDBDao(document_collection)
    document_mongodb_dao.create_document(document)

    return {'meta': META_SUCCESS}
