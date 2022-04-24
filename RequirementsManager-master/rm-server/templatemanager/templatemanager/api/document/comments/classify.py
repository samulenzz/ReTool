import os

from flask import request
from templatemanager.app import app

from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.config import UPLOAD_FILE_DIRNAME
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.comments_classify import classify_comments

META_SUCCESS = {'status': 200, 'msg': '分析成功！'}
META_WRONG_FORMAT = {'status': 400, 'msg': '数据格式错误！'}
META_ERROR = {'status': 404, 'msg': '评论数据不存在！'}


@app.route('/document/comments/classify', methods=['POST'])
@handle_response
def comments_classify():
    body = request.json

    comments_file_name = body['comments_file_name']

    file_path = os.path.join(UPLOAD_FILE_DIRNAME, f'{comments_file_name}.csv')

    if not os.path.exists(file_path):
        return {'meta': META_ERROR}

    try:
        classify_result = classify_comments(file_path)
    except Exception as e:
        print(e)
        import traceback
        print(traceback.print_exc())
        return {'meta': META_WRONG_FORMAT}

    return {
        'meta': META_SUCCESS,
        'data': {
            'classify_result': classify_result
        }
    }
