from datetime import datetime

from flask import request

from requirementmanager.app import app
from requirementmanager.mongodb import (
    requirement_collection, requirement_tree_collection
)
from requirementmanager.dao.requirement import (
    Requirement, RequirementMongoDBDao
)
from requirementmanager.dao.requirement_tree import (
    RequirementTree, RequirementTreeNode, RequirementTreeMongoDBDao
)
from requirementmanager.utils.handle_api import handle_response, verify_request
from requirementmanager.utils.client_username import get_client_username


META_SUCCESS = {'status': 200, 'msg': '创建成功！'}


@app.route('/requirement/create', methods=['POST'])
@verify_request(['access'], access='requirement_create')
@handle_response
def requirement_create():
    body = request.json
    # 自动补全author , created_time , last_modify_time
    body['author'] = get_client_username()
    body['created_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body['last_modify_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    project_id = body['project_id']
    base_id = body.pop('base_id')
    location = body.pop('location')

    requirement_dao = RequirementMongoDBDao(requirement_collection)
    requirement_tree_dao = RequirementTreeMongoDBDao(
        requirement_tree_collection
    )

    # 创建需求条目
    requirement = Requirement(**body)
    requirement_dao.create(requirement)

    # 向Tree添加需求条目
    tree = requirement_tree_dao.get(project_id)
    # 如果不存在，就创建
    if not tree:
        tree = RequirementTree(project_id)
        requirement_tree_dao.create(tree)
    new_node = RequirementTreeNode(
        _id=requirement._id,
        name=requirement.name,
    )
    requirement_tree_dao.add_tree_node(project_id, new_node, base_id, location)

    # 修改需求条目属性
    _type = requirement_tree_dao.get(project_id).get_node_type(requirement._id)
    requirement_dao.edit(requirement._id, _type=_type)
    return {
        'meta': META_SUCCESS,
        'data': {
            'requirement_id': requirement._id
        }
    }
