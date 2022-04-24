import os

from flask import request
from templatemanager.app import app
from templatemanager.dao.template import (
    Template, TemplateMongoDBDao
)
from templatemanager.mongodb import template_collection
from templatemanager.utils.handle_api import handle_response
from templatemanager.utils.uuid import generate_uuid

from docx import Document
from time import asctime, localtime

META_SUCCESS = {'status': 200, 'msg': '创建成功！'}
META_ERROR_ALREADY_EXIST = {'status': 400, 'msg': '创建失败，该模板已存在！'}
META_ERROR_NO_FILE = {'status': 404, 'msg': '创建失败，文件不存在！'}

UPLOAD_FILE_DIRNAME = 'uploads'
# os.makedirs(UPLOAD_FILE_DIRNAME, exist_ok=True)


def parse_docx(path):
    print(path)
    if not os.path.exists(path):
        return []
    docx = Document(path)
    paragraphs = list(map(lambda x: x.text, docx.paragraphs))
    paragraphs = list(filter(lambda x: len(x) > 0, paragraphs))
    return paragraphs


# if __name__ == '__main__':
#     para = parse_docx('uploads/GJB438B-2009军用软件需求规格说明 模板.docx')
#     print(para)


@app.route('/template/create', methods=['POST'])
@handle_response
# @verify_system_role
def template_create():
    body = request.json

    filetoken = body['token']
    filename = f'{filetoken}.docx'
    filepath = os.path.join(UPLOAD_FILE_DIRNAME, filename)

    # 检测文件是否存在
    if not os.path.exists(filepath):
        return {
            'meta': META_ERROR_NO_FILE
        }
    # parse the docx
    outline = parse_docx(filepath)

    template_name = filetoken
    introduction = body['introduction']

    template_mongodb_dao = TemplateMongoDBDao(template_collection)
    # check if template exists
    if template_mongodb_dao.get_template(template_name):
        return {'meta': META_ERROR_ALREADY_EXIST}

    template = Template(_id=generate_uuid(),
                        template_name=template_name,
                        introduction=introduction,
                        last_time=asctime(localtime()),
                        outline=outline)
    template_mongodb_dao.create_template(template)
    return {'meta': META_SUCCESS}

# from usermanager.app import app
# from usermanager.dao.user import (
#     User, UserMongoDBDao
# )
# from usermanager.mongodb import user_collection
# from usermanager.utils.handle_api import verify_system_role, handle_response
# from usermanager.utils.password import encrypt_password
#
#
# META_SUCCESS = {'status': 200, 'msg': '添加成功！'}
# META_ERROR = {'status': 400, 'msg': '添加失败！该用户已存在！'}
#
#
# @app.route('/user/create', methods=['POST'])
# @handle_response
# @verify_system_role
# def user_create():
#     body = request.json
#     user_mongodb_dao = UserMongoDBDao(user_collection)
#     # Check if user exists
#     if user_mongodb_dao.get_user(body['username']):
#         return {'meta': META_ERROR}
#     # Encrypt password
#     body['password'] = encrypt_password(body['password'])
#     user = User(**body)
#     user_mongodb_dao.create_user(user)
#     return {'meta': META_SUCCESS}
