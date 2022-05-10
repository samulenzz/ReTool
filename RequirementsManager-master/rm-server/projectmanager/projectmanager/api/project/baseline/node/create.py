from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    baseline_collection
)
from projectmanager.dao.baseline import (
    BaselineNode, BaselineMongoDBDao
)
from projectmanager.utils.handle_api import handle_response, verify_request
from projectmanager.utils.client_username import get_client_username
from projectmanager.http_client import requirementmanager_http_client

META_SUCCESS = {'status': 200, 'msg': '创建成功！'}
META_ERROR = {'status': 400, 'msg': "创建失败！当前项目需求为空，请先添加需求！"}


@app.route('/project/baseline/node/create', methods=['POST'])
@verify_request(['project', 'access'], access='project_baseline_node_create')
@handle_response
def project_baseline_node_create():
    body = request.json
    project_id = body.pop('project_id')
    client_username = get_client_username()

    baseline_dao = BaselineMongoDBDao(baseline_collection)

    # 创建节点
    node = BaselineNode(**body, author=client_username)

    # 调用需求管理服务的需求条目归档
    resp_body = requirementmanager_http_client.requirement_archive_create(
        project_id, node.version
    )

    if resp_body['meta']['status'] != 200:
        return {
            'meta': META_ERROR
        }

    # 添加节点
    baseline_dao.add_node(project_id, node)

    return {
        'meta': META_SUCCESS,
    }
