import os

from flask import request
from templatemanager.app import app

from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.comments_similarity import cluster_by_similarity

META_SUCCESS = {'status': 200, 'msg': '分析成功！'}


@app.route('/document/comments/similarity', methods=['POST'])
@handle_response
def comments_similarity():
    body = request.json

    classifyResult = body['classify_result']
    aspect = body['aspect']
    label = body['label']

    commentsDictList = classifyResult[aspect][label]

    res = cluster_by_similarity(commentsDictList)

    classifyResult[aspect][label] = res

    return {
        'meta': META_SUCCESS,
        'data': {
            'classify_result': classifyResult
        }
    }
