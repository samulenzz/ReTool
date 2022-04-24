import json

from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    requirement_collection, archive_requirement_collection
)
from requirementmanager.dao.requirement_list import RequirementListMongoDBDao
from requirementmanager.dao.archive import ArchiveRequirementListMongoDBDao
from requirementmanager.utils.handle_api import handle_response
from requirementmanager.api.requirement.analyze._utils import (
    wrap_add_single_requirement, wrap_tree_requirements,
    wrap_edit_single_requirement, wrap_compared_requirements
)
from requirementmanager.grpc_client.client import GrpcClient


RELATIONSHIP_TYPE_MAP = {
    '0': '前提关系',
    '4': '交互关系',
}

META_SUCCESS = {'status': 200, 'msg': '关联关系分析成功！'}


@app.route('/requirement/analyze/relationship', methods=['POST'])
@handle_response
def requirement_analyze_relationship():
    body = request.json
    target_data = body['target_data']
    # 分析需求的类型，值为add_single, tree, edit_single，针对不同类型会有不同的wrap方式
    target_type = body['target_type']
    scope = body['scope']  # {"project_id": str, "version": str}

    # 如果version为None，则说明是当前版本，使用requirement_collection
    # 否则为归档版本
    if not scope['version']:
        requirement_list_dao = RequirementListMongoDBDao(
            requirement_collection
        )
        compared_reqs_list = requirement_list_dao.get_requirement_list(
            project_id=scope['project_id']
        )
    else:
        requirement_list_dao = ArchiveRequirementListMongoDBDao(
            archive_requirement_collection
        )
        compared_reqs_list = requirement_list_dao.get_requirement_list(
            project_id=scope['project_id'], version=scope['version']
        )

    # wrap target_data
    if target_type == 'add_single':
        target_reqs_dict = wrap_add_single_requirement(target_data)
    elif target_type == 'tree':
        target_reqs_dict = wrap_tree_requirements(target_data)
    elif target_type == 'edit_single':
        target_reqs_dict = wrap_edit_single_requirement(target_data)

    # wrap compared_reqs_list
    compared_reqs_dict = wrap_compared_requirements(compared_reqs_list)

    # 合并成一个dict，转换成列表，调用grpc获取结果
    sum_reqs_dict = dict(compared_reqs_dict, **target_reqs_dict)
    sum_reqs_list = [req for req in sum_reqs_dict.values()]

    # 调用grpc
    resp = GrpcClient().relationship(json.dumps({'items': sum_reqs_list}))
    resp = json.loads(resp)
    print(resp)

    # wrap 返回结果
    res = []
    response_id_pairs = set()
    for item in resp['result']:
        id0 = item['id1']
        id1 = item['id2']
        if (id0 not in target_reqs_dict) and (id1 not in target_reqs_dict):
            continue
        # 过滤掉重复的结果
        if ((id0, id1) in response_id_pairs) or ((id1, id0) in response_id_pairs):
            continue
        if id0 in target_reqs_dict:
            req0 = {
                'name': target_reqs_dict[id0]['name'],
                'description': target_reqs_dict[id0]['description'],
            }
        else:
            req0 = {
                'name': compared_reqs_dict[id0]['name'],
                'description': compared_reqs_dict[id0]['description'],
            }
        if id1 in target_reqs_dict:
            req1 = {
                'name': target_reqs_dict[id1]['name'],
                'description': target_reqs_dict[id1]['description'],
            }
        else:
            req1 = {
                'name': compared_reqs_dict[id1]['name'],
                'description': compared_reqs_dict[id1]['description'],
            }
        res.append({
            '_type': RELATIONSHIP_TYPE_MAP[item['relationType']],
            'req0': req0,
            'req1': req1,
        })
        response_id_pairs.add((id0, id1))

    return {
        'meta': META_SUCCESS,
        'data': res
    }
