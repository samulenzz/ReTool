from flask import request

from projectmanager.app import app
from projectmanager.mongodb import (
    baseline_collection
)
from projectmanager.dao.baseline import (
    BaselineMongoDBDao
)
from projectmanager.utils.handle_api import handle_response, verify_request


META_SUCCESS = {'status': 200, 'msg': '获取成功！'}


@app.route('/project/baseline/node/list', methods=['GET'])
@verify_request(['project', 'access'], access='project_baseline_node_list')
@handle_response
def project_baseline_node_list():
    project_id = request.args.get('project_id')

    baseline_dao = BaselineMongoDBDao(baseline_collection)

    # 获取节点列表
    nodes = baseline_dao.get_all_nodes(project_id)
    res = [node.jsonify() for node in nodes]
    return {
        'meta': META_SUCCESS,
        'data': res
    }
