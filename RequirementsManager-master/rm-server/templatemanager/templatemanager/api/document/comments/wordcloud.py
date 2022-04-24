import os

from flask import request
from templatemanager.app import app
from templatemanager.dao.document import (
    Document, DocumentMongoDBDao
)
from templatemanager.mongodb import document_collection
from templatemanager.config import UPLOAD_FILE_DIRNAME
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.comments_wordcloud import generateWordCloudBase64

META_SUCCESS = {'status': 200, 'msg': '词云生成成功！'}
META_WRONG_FORMAT = {'status': 400, 'msg': '数据格式错误！'}
META_ERROR_BAD_FILE = {'status': 404, 'msg': '生成失败，评论集不存在！'}


@app.route('/document/comments/wordcloud', methods=['GET'])
@handle_response
def comments_wordcloud():
    # body = request.json

    # comments_file_name = body['comments_file_name']
    comments_file_name = request.args.get('comments_file_name')

    file_path = os.path.join(UPLOAD_FILE_DIRNAME, f'{comments_file_name}.csv')

    if not os.path.exists(file_path):
        return {'meta': META_ERROR_BAD_FILE}

    try:
        img_base64_str = generateWordCloudBase64(file_path)
    except Exception as e:
        print(e)
        import traceback
        print(traceback.print_exc())
        return {'meta': META_WRONG_FORMAT}

    return {
        'meta': META_SUCCESS,
        "data": {
            'img_base64': img_base64_str
        }
    }
