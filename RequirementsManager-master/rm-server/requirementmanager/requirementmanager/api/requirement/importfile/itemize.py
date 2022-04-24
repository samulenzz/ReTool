import os
from typing import List

from flask import request

from requirementmanager.app import app
from requirementmanager.utils.handle_api import handle_response
from requirementmanager.utils.parse_docx import (
    parse_docx, generate_elementui_tree
)
from requirementmanager.utils.wrap_elementui_tree import add_section_number
from requirementmanager.dao.requirement_tree import REQUIREMENT_TYPE_MAP


META_SUCCESS = {'status': 200, 'msg': '条目化成功！'}
META_ERROR_NO_FILE = {'status': 404, 'msg': '条目化失败，文件不存在！'}

UPLOAD_FILE_DIRNAME = 'uploads'
os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)


def wrap_resp_data(resp_data: List) -> List:
    res = []
    for key, value in REQUIREMENT_TYPE_MAP.items():
        res.append({
            '_id': key, 'label': value, 'children': []
        })

    for item in resp_data:
        for node in res:
            if item['label'] == node['label']:
                node['children'] = item['children']
    return res


@app.route('/requirement/importfile/itemize', methods=['POST'])
@handle_response
def requirement_importfile_itemize():
    body = request.json
    filetoken = body['token']
    filename = f'{filetoken}.docx'
    filepath = os.path.join(UPLOAD_FILE_DIRNAME, filename)

    # 检测文件是否存在
    if not os.path.exists(filepath):
        return {
            'meta': META_ERROR_NO_FILE
        }

    # 进行条目化
    docx_section = parse_docx(filepath)
    tree_root_node = generate_elementui_tree(docx_section)
    resp_data = tree_root_node['children']
    resp_data = wrap_resp_data(resp_data)

    add_section_number(resp_data, 1)

    return {
        'meta': META_SUCCESS,
        'data': resp_data
    }
